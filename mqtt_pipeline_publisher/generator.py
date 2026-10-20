# --- generator.py ---
import time
import numpy as np
from config import settings

class SensorDataGenerator:
    @staticmethod
    def generate():
        timestamp = int(time.time())
        temp = np.random.normal(loc=25, scale=5)
        pres = temp * settings.PRESSURE_SLOPE + np.random.normal(loc=0, scale=settings.PRESSURE_NOISE_STD)

        # 25% chance of anomaly
        if np.random.rand() < 0.25:
            temp = np.random.choice([np.random.uniform(5,14), np.random.uniform(61,90)])
            pres = temp * settings.PRESSURE_SLOPE + np.random.normal(loc=0.7, scale=0.2)

        return timestamp, temp, pres