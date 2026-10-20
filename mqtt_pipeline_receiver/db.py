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
        self._ensure_schema()

    def _ensure_schema(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                ALTER TABLE sensor_data ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
                ALTER TABLE sensor_data ADD COLUMN IF NOT EXISTS anomaly_value INTEGER DEFAULT 0;
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id SERIAL PRIMARY KEY,
                    timestamp BIGINT,
                    temperature DOUBLE PRECISION,
                    pressure DOUBLE PRECISION,
                    anomaly_value INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS anomaly_logs (
                    id SERIAL PRIMARY KEY,
                    timestamp BIGINT,
                    temperature DOUBLE PRECISION,
                    pressure DOUBLE PRECISION
                );
                """
            )
            self.conn.commit()

    def insert_sensor(self, ts: int, temp: float, pres: float) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sensor_data (timestamp, temperature, pressure, anomaly_value) VALUES (%s, %s, %s, 0) RETURNING id",
                (ts, temp, pres)
            )
            row_id = cur.fetchone()[0]
            self.conn.commit()
            return row_id

    def update_anomaly(self, row_id: int, value: int):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE sensor_data SET anomaly_value = %s WHERE id = %s",
                (value, row_id)
            )
            self.conn.commit()