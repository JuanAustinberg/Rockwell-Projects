# --- db.py ---
import psycopg2
from psycopg2.extensions import connection as _connection
from config import settings

class Database:
    def __init__(self):
        self.conn: _connection = psycopg2.connect(
            host=settings.PG_HOST,
            port=settings.PG_PORT,
            dbname=settings.PG_DB,
            user=settings.PG_USER,
            password=settings.PG_PASS
        )
        self._ensure_tables()

    def _ensure_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    timestamp BIGINT,
                    temperature DOUBLE PRECISION,
                    pressure DOUBLE PRECISION
                );
                CREATE TABLE IF NOT EXISTS anomaly_logs (
                    timestamp BIGINT,
                    temperature DOUBLE PRECISION,
                    pressure DOUBLE PRECISION
                );
                '''
            )
            self.conn.commit()

    def insert_sensor(self, timestamp: int, temperature, pressure):
        # Ensure values are Python native types
        temperature = float(temperature)
        pressure = float(pressure)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sensor_data (timestamp, temperature, pressure) VALUES (%s, %s, %s)",
                (timestamp, temperature, pressure)
            )
            self.conn.commit()
