# --- mqtt_client.py ---
import json
import paho.mqtt.client as mqtt
from config import settings
from logger import logger

class MQTTClient:
    def __init__(self):
        # Instantiate client without unsupported callback_api_version
        self.client = mqtt.Client(client_id="sensor_publisher")
        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
        logger.info(f"Connected to MQTT broker at {settings.MQTT_BROKER}:{settings.MQTT_PORT}")

    def publish(self, topic: str, payload: dict):
        self.client.publish(topic, json.dumps(payload))
        logger.info(f"Published: {payload} to topic: {topic}")
