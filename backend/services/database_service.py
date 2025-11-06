from fastapi import HTTPException
import mariadb
from dotenv import load_dotenv
import os
import json

load_dotenv()

# MariaDB config
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection error: {e}")

def log_assumption_to_db(ai_model: str, data: dict):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        data_json = json.dumps(data)
        
        query = """
            INSERT INTO assumption (ai_model, data)
            VALUES (?, ?)
        """
        cur.execute(query, (ai_model, data_json))
        conn.commit()
        
        assumption_id = cur.lastrowid
        return assumption_id
        
    finally:
        cur.close()
        conn.close()

