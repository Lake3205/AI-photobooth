
from services.auth_service import create_access_token
from datetime import timedelta, datetime, timezone
from services.database_service import DatabaseService
from fastapi import HTTPException, status
from jose import JWTError, jwt
from dotenv import load_dotenv
from os import getenv
from models.assumptions import AssumptionsModel

class FormService:
    load_dotenv()
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.expiration_time = timedelta(days=1)
        self.secret_key = getenv("JWT_SECRET_KEY")
        self.algorithm = getenv("ALGORITHM", "HS256")
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    def create_form_token(self, assumption_id: int):
        return create_access_token(data={"sub": str(assumption_id)}, expires_delta=self.expiration_time)
    
    def get_token_data(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise self.credentials_exception
        
    def verify_form_token(self, token: str):
        conn = None
        cur = None
        
        try:
            payload = self.get_token_data(token)
            
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            assumption_id = int(payload.get("sub"))
            
            query = """
            SELECT assumption_id FROM form_tokens
            WHERE token = ? AND assumption_id = ? AND used = 0
            """
            
            cur.execute(query, (token, assumption_id))
            
            if cur.rowcount == 0:
                raise Exception("Form token not found")
            if cur.rowcount > 1:
                raise Exception("Multiple form tokens found")
            
            return True
        except JWTError:
            raise self.credentials_exception
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)
        
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
            
    def get_assumptions_by_token(self, token: str):
        conn = None
        cur = None
        
        try:
            payload = self.get_token_data(token)
            
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            assumption_id = int(payload.get("sub"))
            assumptions_model = AssumptionsModel()
            
            query = """
            SELECT ac.id, ac.value, av.value, av.reasoning
            FROM assumptions a
            LEFT JOIN assumption_values av ON a.id = av.assumption_id
            JOIN assumption_constants ac ON av.assumption_constant_id = ac.id
            JOIN form_tokens ft ON a.id = ft.assumption_id
            WHERE ft.token = ? AND ft.assumption_id = ? AND ft.used = 0
            """
            
            cur.execute(query, (token, assumption_id))
            
            result = cur.fetchall()
            if not result:
                raise Exception("No assumptions found for the provided token")
            
            for row in result:
                (id, assumption, value, reasoning) = row
                if (assumption in assumptions_model.assumptions):
                    assumptions_model.assumptions[assumption]["value"] = value
                    assumptions_model.assumptions[assumption]["reasoning"] = reasoning
            
            return assumptions_model.assumptions
        except JWTError:
            raise self.credentials_exception
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)
    