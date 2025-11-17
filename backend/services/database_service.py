from fastapi import HTTPException
import mariadb
from models.assumptions import AssumptionsModel
import config  # Load environment configuration

class DatabaseSingleton:
    def __init__(self):
        self.db_config = {
            "user": config.DB_USER,
            "password": config.DB_PASSWORD,
            "host": config.DB_HOST,
            "port": config.DB_PORT,
            "database": config.DB_NAME,
            "connect_timeout": 5,
            "autocommit": False
        }
    
    def get_connection(self):
        try:
            conn = mariadb.connect(**self.db_config)
            return conn
        except mariadb.Error as e:
            raise HTTPException(status_code=500, detail=f"DB connection error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected DB error: {e}")
    
    def close_resources(self, cursor=None, connection=None):
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"Error closing cursor: {e}")
        if connection:
            try:
                connection.close()
            except Exception as e:
                print(f"Error closing connection: {e}")

    def log_assumption(self, ai_model: str, data: dict):
        conn = None
        cur = None
        
        try:
            conn = self.get_connection()
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
                    INSERT INTO assumption_values (assumption_id, assumption_constant_id, value, reasoning)
                    VALUES (?, ?, ?, ?)
                """
                cur.execute(value_query, (assumption_id, constant_id, str(value["value"]) if value is not None else None, value["reasoning"]))
            
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
            self.close_resources(cur, conn)

    def get_assumptions_by_model(self, ai_model: str):
        conn = self.get_connection()
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
            
            return self._format_assumptions(rows)
        finally:
            self.close_resources(cur, conn)

    def _format_assumptions(self, rows):
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
    
    def get_all_assumptions(self):
        conn = self.get_connection()
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
            
            return self._format_assumptions(rows)
        finally:
            self.close_resources(cur, conn)

    def get_assumption_constants(self):
        conn = self.get_connection()
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
            self.close_resources(cur, conn)

    def get_formats(self):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            query = "SELECT id, value FROM formats ORDER BY value"
            cur.execute(query)
            rows = cur.fetchall()
            
            return [{"id": row[0], "value": row[1]} for row in rows]
        finally:
            self.close_resources(cur, conn)

    def delete_assumption(self, assumption_id: int):
        conn = None
        cur = None
        
        try:
            conn = self.get_connection()
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
            self.close_resources(cur, conn)

    def get_user_by_username(self, username: str):
        conn = None
        cur = None
        
        try:
            conn = self.get_connection()
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
            self.close_resources(cur, conn)

class DatabaseService:
    _instance = None
    _db_singleton = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._db_singleton = DatabaseSingleton()
        return cls._instance

    def get_db_connection(self):
        return self._db_singleton.get_connection()
    
    def close_resources(self, cursor=None, connection=None):
        self._db_singleton.close_resources(cursor, connection)

    def log_assumption_to_db(self, ai_model: str, data: dict):
        return self._db_singleton.log_assumption(ai_model, data)

    def get_assumptions_by_model(self, ai_model: str):
        return self._db_singleton.get_assumptions_by_model(ai_model)

    def get_all_assumptions(self):
        return self._db_singleton.get_all_assumptions()

    def get_assumption_constants(self):
        return self._db_singleton.get_assumption_constants()

    def get_formats(self):
        return self._db_singleton.get_formats()

    def delete_assumption(self, assumption_id: int):
        return self._db_singleton.delete_assumption(assumption_id)

    def get_user_by_username(self, username: str):
        return self._db_singleton.get_user_by_username(username)
