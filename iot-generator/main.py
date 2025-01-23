import json
import random
import time
import os

import paho.mqtt.publish as publish

host = os.environ.get('MQTT_HOST', 'broker')


def generator_1():
    return {'temp': random.randint(25, 29),
            'humid': random.randint(24, 29),
            'BAT': random.randint(90, 100)
            }


def generator_2():
    return {'temp': random.randint(10, 22),
            'vdd': random.randint(35000, 35200),
            'BAT': random.randint(30, 35)
            }


def generator_no_bat():
    return {'temp': random.randint(25, 29),
            'humid': random.randint(24, 29),
            'NOT': random.randint(90, 100),
            'status': 'OK'
            }


devices = [('UPB/Zeus', generator_1), ('UPB/Kali', generator_2), ('CFRO/Garo', generator_no_bat)]


def send_yesterday():
    import datetime
    start = datetime.datetime.now(datetime.timezone.utc).astimezone()
    current = start - datetime.timedelta(days=1)
    while current <= start:
        for d in devices:
            payload = d[1]()

            topic = d[0]
            payload['timestamp'] = current.strftime('%Y-%m-%dT%H:%M:%S+03:00')
            json_payload = json.dumps(payload)
            print('{} - {}'.format(topic, json_payload))

            publish.single(topic, payload=json_payload, hostname=host, qos=2)

        current = current + datetime.timedelta(minutes=15)


def main():
    print('Using {} as broker.'.format(host))

    print('Flooding yesterday')
    send_yesterday()

    print('Now we add new data every 5 seconds...')
    while True:
        for d in devices:
            payload = d[1]()
            json_payload = json.dumps(payload)
            topic = d[0]
            print('{} - {}'.format(topic, json_payload))
            publish.single(topic, payload=json_payload, hostname=host, qos=2)

        time.sleep(5)


if __name__ == '__main__':
    main()
