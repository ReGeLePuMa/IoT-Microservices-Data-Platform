import paho.mqtt.client as mqtt
import json
import os
from logger import logger
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

db_url = os.getenv("INFLUXDB_URL", "http://localhost:8086")
db_token = os.getenv("INFLUXDB_TOKEN", "my-token")
db_org = os.getenv("INFLUXDB_ORG", "my-org")

influx_client = InfluxDBClient(
    url=db_url,
    token=db_token,
    org=db_org
)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)

class MQTTChatClient:
    def __init__(self, broker_address, broker_port, topic_subscribe):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic_subscribe = topic_subscribe
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to broker!")
            client.subscribe(self.topic_subscribe)
        else:
            logger.error(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = json.loads(msg.payload)
        logger.info(f"Received a message by topic [{topic}]")

        timestamp = data.get("timestamp", datetime.now().isoformat())
        logger.info(f"Data timestamp is{f': {timestamp}' if data.get('timestamp') else ' NOW'}")

        location, station = topic.split("/")
        for key, value in data.items():
            if isinstance(value, (int, float)):
                write_api.write("tema3", db_org, 
                [
                    {
                        "measurement": f"{location}.{station}.{key}",
                        "tags": {
                            "location": location,
                            "station": station
                        },
                        "fields": {
                            "value": float(value)
                        },
                        "time": timestamp
                    }
                ])
                logger.info(f"{location}.{station}.{key} {value}")
        logger.info("")

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)

    def start(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Disconnecting from broker...")
            self.client.disconnect()


if __name__ == "__main__":
    broker_address = os.getenv("BROKER_HOST", "localhost")
    broker_port = int(os.getenv("BROKER_PORT", "1883"))

    chat_client = MQTTChatClient(broker_address, broker_port, "#")
    chat_client.connect()
    chat_client.start()