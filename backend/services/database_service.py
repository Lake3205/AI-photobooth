from fastapi import HTTPException
import mariadb
from dotenv import load_dotenv
import os
from models.assumptions import AssumptionsModel

load_dotenv()

# MariaDB config
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME"),
    "connect_timeout": 5,
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
        
        # Insert into assumptions table
        query = """
            INSERT INTO assumptions (ai_model)
            VALUES (?)
        """
        cur.execute(query, (ai_model,))
        assumption_id = cur.lastrowid
        
        # Insert assumption values for each data item
        for key, value in data.items():
            # First, get or create the assumption constant
            constant_query = """
                SELECT id FROM assumption_constants WHERE value = ?
            """
            cur.execute(constant_query, (key,))
            constant_row = cur.fetchone()
            
            if constant_row:
                constant_id = constant_row[0]
            else:
                assumptions_model = AssumptionsModel()
                # Default format is "text"
                format_value = assumptions_model.assumptions.get(key, {}).get("format", "text")
                
                format_query = "SELECT id FROM formats WHERE value = ?"
                cur.execute(format_query, (format_value,))
                format_row = cur.fetchone()
                
                if format_row:
                    format_id = format_row[0]
                else:
                    insert_format_query = "INSERT INTO formats (value) VALUES (?)"
                    cur.execute(insert_format_query, (format_value,))
                    format_id = cur.lastrowid
                
                insert_constant_query = """
                    INSERT INTO assumption_constants (value, format_id)
                    VALUES (?, ?)
                """
                cur.execute(insert_constant_query, (key, format_id))
                constant_id = cur.lastrowid
            
            value_query = """
                INSERT INTO assumption_values (assumption_id, assumption_constant_id, value)
                VALUES (?, ?, ?)
            """
            cur.execute(value_query, (assumption_id, constant_id, str(value) if value is not None else None))
        
        conn.commit()
        return assumption_id
        
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception as rollback_error:
                print(f"Error during rollback: {rollback_error}")
        raise
    finally:
        if cur:
            try:
                cur.close()
            except Exception as close_cur_error:
                print(f"Error closing cursor: {close_cur_error}")
        if conn:
            try:
                conn.close()
            except Exception as close_conn_error:
                print(f"Error closing connection: {close_conn_error}")

def get_assumptions_by_model(ai_model: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Get all assumptions for the specified model with their values
        query = """
            SELECT 
                a.id, 
                a.ai_model, 
                a.created_at,
                ac.value as constant_name,
                av.value as assumption_value
            FROM assumptions a
            LEFT JOIN assumption_values av ON a.id = av.assumption_id
            LEFT JOIN assumption_constants ac ON av.assumption_constant_id = ac.id
            WHERE a.ai_model = ?
            ORDER BY a.created_at DESC, ac.value
        """
        cur.execute(query, (ai_model,))
        rows = cur.fetchall()
        
        if not rows:
            return []
        
        assumptions_model = AssumptionsModel()
        
        # Group assumptions by id
        assumptions_dict = {}
        for row in rows:
            assumption_id = row[0]
            ai_model_name = row[1]
            created_at = row[2]
            constant_name = row[3]
            assumption_value = row[4]
            
            if assumption_id not in assumptions_dict:
                assumptions_dict[assumption_id] = {
                    "id": assumption_id,
                    "ai_model": ai_model_name,
                    "created_at": created_at,
                    "values": {}
                }
            
            # Add the constant value if it exists
            if constant_name and assumption_value is not None:
                assumptions_dict[assumption_id]["values"][constant_name] = assumption_value
        
        # Format the results
        assumptions = []
        for assumption_data in assumptions_dict.values():
            formatted_assumptions = {}
            for key, format_data in assumptions_model.assumptions.items():
                value = assumption_data["values"].get(key)
                # Try to convert numeric values back to their proper types
                if value is not None:
                    if format_data["format"] in ["percentage", "number", "weight", "years"]:
                        try:
                            if format_data["format"] == "percentage":
                                value = float(value)
                            else:
                                value = int(value)
                        except (ValueError, TypeError):
                            pass  # Keep as string if conversion fails
                    elif format_data["format"] in ["currency"]:
                        try:
                            value = int(value)
                        except (ValueError, TypeError):
                            pass
                
                formatted_assumptions[key] = {
                    "name": format_data["name"],
                    "format": format_data["format"],
                    "value": value
                }
            
            assumptions.append({
                "id": assumption_data["id"],
                "ai_model": assumption_data["ai_model"],
                "assumptions": formatted_assumptions,
                "date_created": assumption_data["created_at"]
            })
        
        return assumptions
    finally:
        try:
            cur.close()
        except Exception as close_cur_error:
            print(f"Error closing cursor: {close_cur_error}")
        try:
            conn.close()
        except Exception as close_conn_error:
            print(f"Error closing connection: {close_conn_error}")

def get_all_assumptions():
    """Get all assumptions from the database"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Get all assumptions with their values
        query = """
            SELECT 
                a.id, 
                a.ai_model, 
                a.created_at,
                ac.value as constant_name,
                av.value as assumption_value
            FROM assumptions a
            LEFT JOIN assumption_values av ON a.id = av.assumption_id
            LEFT JOIN assumption_constants ac ON av.assumption_constant_id = ac.id
            ORDER BY a.created_at DESC, ac.value
        """
        cur.execute(query)
        rows = cur.fetchall()
        
        if not rows:
            return []
        
        assumptions_model = AssumptionsModel()
        
        # Group assumptions by id
        assumptions_dict = {}
        for row in rows:
            assumption_id = row[0]
            ai_model_name = row[1]
            created_at = row[2]
            constant_name = row[3]
            assumption_value = row[4]
            
            if assumption_id not in assumptions_dict:
                assumptions_dict[assumption_id] = {
                    "id": assumption_id,
                    "ai_model": ai_model_name,
                    "created_at": created_at,
                    "values": {}
                }
            
            # Add the constant value if it exists
            if constant_name and assumption_value is not None:
                assumptions_dict[assumption_id]["values"][constant_name] = assumption_value
        
        # Format the results
        assumptions = []
        for assumption_data in assumptions_dict.values():
            formatted_assumptions = {}
            for key, format_data in assumptions_model.assumptions.items():
                value = assumption_data["values"].get(key)
                # Try to convert numeric values back to their proper types
                if value is not None:
                    if format_data["format"] in ["percentage", "number", "weight", "years"]:
                        try:
                            if format_data["format"] == "percentage":
                                value = float(value)
                            else:
                                value = int(value)
                        except (ValueError, TypeError):
                            pass  # Keep as string if conversion fails
                    elif format_data["format"] in ["currency"]:
                        try:
                            value = int(value)
                        except (ValueError, TypeError):
                            pass
                
                formatted_assumptions[key] = {
                    "name": format_data["name"],
                    "format": format_data["format"],
                    "value": value
                }
            
            assumptions.append({
                "id": assumption_data["id"],
                "ai_model": assumption_data["ai_model"],
                "assumptions": formatted_assumptions,
                "date_created": assumption_data["created_at"]
            })
        
        return assumptions
    finally:
        try:
            cur.close()
        except Exception as close_cur_error:
            print(f"Error closing cursor: {close_cur_error}")
        try:
            conn.close()
        except Exception as close_conn_error:
            print(f"Error closing connection: {close_conn_error}")

def get_assumption_constants():
    """Get all assumption constants with their format information"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query = """
            SELECT ac.id, ac.value, f.value as format
            FROM assumption_constants ac
            LEFT JOIN formats f ON ac.format_id = f.id
            ORDER BY ac.value
        """
        cur.execute(query)
        rows = cur.fetchall()
        
        return [{"id": row[0], "value": row[1], "format": row[2]} for row in rows]
    finally:
        try:
            cur.close()
        except Exception as close_cur_error:
            print(f"Error closing cursor: {close_cur_error}")
        try:
            conn.close()
        except Exception as close_conn_error:
            print(f"Error closing connection: {close_conn_error}")

def get_formats():
    """Get all formats"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query = "SELECT id, value FROM formats ORDER BY value"
        cur.execute(query)
        rows = cur.fetchall()
        
        return [{"id": row[0], "value": row[1]} for row in rows]
    finally:
        try:
            cur.close()
        except Exception as close_cur_error:
            print(f"Error closing cursor: {close_cur_error}")
        try:
            conn.close()
        except Exception as close_conn_error:
            print(f"Error closing connection: {close_conn_error}")

def delete_assumption(assumption_id: int):
    """Delete an assumption and all its related data"""
    conn = None
    cur = None
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Delete assumption (CASCADE will handle assumption_values and forms)
        query = "DELETE FROM assumptions WHERE id = ?"
        cur.execute(query, (assumption_id,))
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Assumption not found")
        
        conn.commit()
        return {"message": f"Assumption {assumption_id} deleted successfully"}
        
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception as rollback_error:
                print(f"Error during rollback: {rollback_error}")
        raise
    finally:
        if cur:
            try:
                cur.close()
            except Exception as close_cur_error:
                print(f"Error closing cursor: {close_cur_error}")
        if conn:
            try:
                conn.close()
            except Exception as close_conn_error:
                print(f"Error closing connection: {close_conn_error}")

def get_user_by_username(username: str):
    conn = None
    cur = None
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id, username, hashed_password, role
            FROM users
            WHERE username = ?
        """
        cur.execute(query, (username,))
        row = cur.fetchone()
        
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "hashed_password": row[2],
                "role": row[3] if len(row) > 3 else "admin"
            }
        return None
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if cur:
            try:
                cur.close()
            except Exception as close_cur_error:
                print(f"Error closing cursor: {close_cur_error}")
        if conn:
            try:
                conn.close()
            except Exception as close_conn_error:
                print(f"Error closing connection: {close_conn_error}")
