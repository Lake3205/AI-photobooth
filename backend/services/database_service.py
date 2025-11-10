from fastapi import HTTPException
import mariadb
from dotenv import load_dotenv
import os
import json
from models.assumptions import AssumptionsModel

load_dotenv()

# MariaDB config
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME"),
    "connect_timeout": 5,  # 5 second connection timeout
    "autocommit": False
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected DB error: {e}")

def log_assumption_to_db(ai_model: str, data: dict):
    conn = None
    cur = None
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        data_json = json.dumps(data)
        
        query = """
            INSERT INTO assumption (ai_model, data)
            VALUES (?, ?)
        """
        cur.execute(query, (ai_model, data_json))
        conn.commit()
        
        assumption_id = cur.lastrowid
        return assumption_id
        
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        raise
    finally:
        if cur:
            try:
                cur.close()
            except Exception:
                pass
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def get_assumptions_by_model(ai_model: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT id, ai_model, data, date_created
            FROM assumption
            WHERE ai_model = ?
            ORDER BY date_created DESC
        """
        cur.execute(query, (ai_model,))
        rows = cur.fetchall()
        
        assumptions_model = AssumptionsModel()
        
        assumptions = []
        for row in rows:
            assumption_values = json.loads(row[2])
            
            formatted_assumptions = {}
            for key, format_data in assumptions_model.assumptions.items():
                formatted_assumptions[key] = {
                    "name": format_data["name"],
                    "format": format_data["format"],
                    "value": assumption_values.get(key)
                }
            
            assumptions.append({
                "id": row[0],
                "ai_model": row[1],
                "assumptions": formatted_assumptions,
                "date_created": row[3]
            })
        
        return assumptions
    finally:
        cur.close()
        conn.close()

