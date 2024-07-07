import os
import sqlite3

DB_FILE_PATH = os.getenv("DB_FILE_PATH", "records.db")

class DB_Helper:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_FILE_PATH)
        self._drop_stocks_infor_table()
        self._create_stocks_info_table()
    
    def _drop_stocks_infor_table(self):
        cursor = self.conn.cursor()
        query = "DROP TABLE IF EXISTS STOCKS;"
        cursor.execute(query)
        cursor.close()
    
    def _create_stocks_info_table(self):
        cursor = self.conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS STOCKS 
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                company_name TEXT NOT NULL,
                exchange TEXT NOT NULL,
                isin_number TEXT NOT NULL,
                date_of_listing DATE NOT NULL,
                type TEXT NOT NULL,
                face_value INT NOT NULL)"""
        cursor.execute(query)
        cursor.close()
    
    def insert_stocks_info(self, data: list[dict]):
        cursor = self.conn.cursor()
        query = f"""INSERT INTO STOCKS
                (symbol, company_name, exchange, isin_number, date_of_listing, type, face_value)
                VALUES (?,?,?,?,?,?,?)"""
        for row in data:
            values = (row.get("symbol"),
                      row.get("company_name"),
                      row.get("exchange"),
                      row.get("isin_number"),
                      row.get("date_of_listing"),
                      row.get("type"),
                      row.get("face_value"), )
            cursor.execute(query,values)
        self.conn.commit()
        cursor.close()
