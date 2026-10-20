# --- mqtt_subscriber.py ---
import json
import time
import numpy as np
import paho.mqtt.client as mqtt
from config import settings
from logger import logger
from db import Database
from pipeline import AnomalyPipeline

class MQTTSubscriber:
    def __init__(self):
        self.client = mqtt.Client(client_id="anomaly_detector")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.db = Database()
        self.pipeline = AnomalyPipeline()
        self.buffer = []

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
            client.subscribe(settings.SUBSCRIBE_TOPIC)
            logger.info(f"Subscribed to {settings.SUBSCRIBE_TOPIC}")
        else:
            logger.error(f"Connection failed with rc={rc}")

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        ts = payload.get('timestamp')
        temp = payload.get('temperature')
        pres = payload.get('pressure')
        if None in (ts, temp, pres):
            logger.warning(f"Incomplete data: {payload}")
            return

        row_id = self.db.insert_sensor(ts, float(temp), float(pres))
        self.buffer.append({'id': row_id, 'temperature': temp, 'pressure': pres})

        if len(self.buffer) >= settings.BATCH_SIZE:
            arr = np.array([[d['temperature'], d['pressure']] for d in self.buffer])
            preds = self.pipeline.predict_batch(arr)

            for rec, p in zip(self.buffer, preds):
                val = 1 if p == -1 else 0
                self.db.update_anomaly(rec['id'], val)
                if p == -1:
                    anomaly_msg = json.dumps({
                        'timestamp': int(time.time()),
                        'temperature': rec['temperature'],
                        'pressure': rec['pressure']
                    })
                    client.publish(settings.ANOMALY_TOPIC, anomaly_msg)
                    logger.info(f"Published anomaly: {anomaly_msg}")
            self.buffer.clear()

    def run(self):
        logger.info(f"Connecting to broker {settings.MQTT_BROKER}:{settings.MQTT_PORT}...")
        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
        self.client.loop_forever()