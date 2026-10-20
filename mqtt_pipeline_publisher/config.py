# --- config.py ---
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
    PUBLISH_TOPIC: str = os.getenv("PUBLISH_TOPIC", "dataLive")
    PUBLISH_INTERVAL: float = float(os.getenv("PUBLISH_INTERVAL", 1.0))

    PG_HOST: str = os.getenv("PG_HOST", "localhost")
    PG_PORT: int = int(os.getenv("PG_PORT", 5432))
    PG_DB: str = os.getenv("PG_DB", "postgres")
    PG_USER: str = os.getenv("PG_USER", "postgres")
    PG_PASS: str = os.getenv("PG_PASS", "timescaledb")

    PRESSURE_SLOPE: float = float(os.getenv("PRESSURE_SLOPE", 0.04))
    PRESSURE_NOISE_STD: float = float(os.getenv("PRESSURE_NOISE_STD", 0.05))

settings = Settings()