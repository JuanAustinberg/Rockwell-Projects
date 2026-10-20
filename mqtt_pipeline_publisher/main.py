# --- main.py ---
import time
from config import settings
from db import Database
from generator import SensorDataGenerator
from mqtt_client import MQTTClient
from logger import logger


def run():
    db = Database()
    mqtt = MQTTClient()
    logger.info(f"Connected to MQTT {settings.MQTT_BROKER}:{settings.MQTT_PORT}, publishing on {settings.PUBLISH_TOPIC}")

    while True:
        timestamp, temp, pres = SensorDataGenerator.generate()
        payload = {"timestamp": timestamp, "temperature": temp, "pressure": pres}

        # persist
        db.insert_sensor(timestamp, temp, pres)

        # publish
        mqtt.publish(settings.PUBLISH_TOPIC, payload)


        time.sleep(settings.PUBLISH_INTERVAL)

if __name__ == '__main__':
    run()