import sqlite3
from config import SQLITE_DB

class SQLiteManager:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DB)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS buffer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inverter_id TEXT,
            pv_power REAL,
            grid_power REAL,
            daily_energy REAL,
            total_energy REAL,
            temperature REAL
        )
        """)
        self.conn.commit()

    def insert(self, data):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO buffer (
            inverter_id, pv_power, grid_power,
            daily_energy, total_energy, temperature
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["inverter_id"],
            data["pv_power"],
            data["grid_power"],
            data["daily_energy"],
            data["total_energy"],
            data["temperature"]
        ))
        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM buffer")
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "inverter_id": r[1],
                "pv_power": r[2],
                "grid_power": r[3],
                "daily_energy": r[4],
                "total_energy": r[5],
                "temperature": r[6],
            }
            for r in rows
        ]

    def delete(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM buffer WHERE id=?", (record_id,))
        self.conn.commit()