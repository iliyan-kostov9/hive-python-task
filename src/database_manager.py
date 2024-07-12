import sqlite3
from typing import Literal

from client import Client

DB_PATH: Literal["database/coordinate.db"] = "database/coordinate.db"


class DatabaseManager:
    def __init__(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS serial_data
                     (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER, image_path TEXT)"""
        )
        conn.commit()
        conn.close()

    def insert_coords(self, client: Client) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO serial_data (x, y, image_path) VALUES (?, ?, ?)",
            (client.coordinates.x, client.coordinates.y, client.img_path),
        )
        conn.commit()
        print(
            f"Image: {client.img_path} with coordinates: {client.coordinates.x}, {client.coordinates.y} are saved to database!"
        )
        conn.close()

    def get_all(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT x, y, image_path FROM serial_data")
        records = cursor.fetchall()
        conn.close()

        result = []
        for record in records:
            result.append({"x": record[0], "y": record[1], "image_path": record[2]})

        return result
