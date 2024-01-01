import sqlite3


class DBManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                name TEXT,
                price TEXT,
                savings TEXT
            )
        """)

    def insert_data(self, data):
        self.cursor.execute("""
            INSERT INTO products (name, price, savings)
            VALUES (:name, :price, :savings)
        """, data)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
