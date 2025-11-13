
from services.auth_service import create_access_token
from datetime import timedelta, datetime, timezone
from services.database_service import DatabaseService

class FormService:
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.expiration_time = timedelta(days=1)
        
        
    def create_form_token(self, assumption_id: int):
        return create_access_token(data={"sub": assumption_id}, expires_delta=self.expiration_time)
        
    def log_form_token(self, assumption_id: int):
        conn = None
        cur = None
        
        access_token = self.create_form_token(assumption_id)
        expires_at = datetime.now(timezone.utc) + self.expiration_time
        
        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            query = """
            INSERT INTO form_tokens (token, assumption_id, expires_at)
            VALUES (?, ?, ?)
            """
            
            cur.execute(query, (access_token, assumption_id, expires_at))
            conn.commit()
            
            return access_token
            
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)
    