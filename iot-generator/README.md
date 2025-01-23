# What is this?

This MQTT publisher is provided to facilitate the grading of the 3rd homework.

In order to add it to your current stack refer to the following snippet:

```yaml
services:
  generator:
    image: gitlab.cs.pub.ro:5050/scd/iot-generator
    # image: gitlab.cs.pub.ro:5050/scd/iot-generator:mac for MacOS with ARM
    environment:
      - MQTT_HOST=broker # Change it to your broker DNS
    networks:
      - broker-network # Change as needed
```