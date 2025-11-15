
from services.auth_service import create_access_token
from datetime import timedelta, datetime, timezone
from services.database_service import DatabaseService
from fastapi import HTTPException, status
from jose import JWTError, jwt
from dotenv import load_dotenv
from os import getenv
from models.assumptions import AssumptionsModel

from constants.form_constants import ALLOWED_QUESTIONS

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
        self.form_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid form data",
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
            
            return {
                "assumption_id": assumption_id,
                "valid": True
            }
        except JWTError:
            raise self.credentials_exception
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise self.credentials_exception
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
            
    def submit_form_responses(self, form_data: dict, assumption_id: int):
        conn = None
        cur = None
        
        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            create_form_query = """
            INSERT INTO forms (assumption_id)
            VALUES (?)
            """
            cur.execute(create_form_query, (assumption_id,))
            form_id = cur.lastrowid
            
            # Process each question in the form data
            for question_key, question_data in form_data.items():
                question_text = question_data.get("question", "")
                question_type = question_data.get("type", "")
                answer = question_data.get("answer", "")
                explanation = question_data.get("explanation", "")
                scale = question_data.get("scale", None)
                
                # Get or create form_question_type
                type_query = """
                SELECT id FROM form_question_types
                WHERE value = ?
                """
                cur.execute(type_query, (question_type,))
                type_result = cur.fetchone()
                
                if type_result:
                    question_type_id = type_result[0]
                else:
                    min_val = scale[0] if scale and len(scale) > 0 else None
                    max_val = scale[1] if scale and len(scale) > 1 else None
                    
                    create_type_query = """
                    INSERT INTO form_question_types (value, min, max)
                    VALUES (?, ?, ?)
                    """
                    cur.execute(create_type_query, (question_type, min_val, max_val))
                    question_type_id = cur.lastrowid
                
                question_query = """
                SELECT id FROM form_questions
                WHERE question_type_id = ? AND question = ?
                """
                cur.execute(question_query, (question_type_id, question_text))
                question_result = cur.fetchone()
                
                if question_result:
                    form_question_id = question_result[0]
                else:
                    create_question_query = """
                    INSERT INTO form_questions (question_type_id, question)
                    VALUES (?, ?)
                    """
                    cur.execute(create_question_query, (question_type_id, question_text))
                    form_question_id = cur.lastrowid
                
                insert_result_query = """
                INSERT INTO form_results (form_id, form_question_id, value, explanation)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(insert_result_query, (form_id, form_question_id, answer, explanation if explanation else None))
            
            # Mark the token as used
            update_token_query = """
            UPDATE form_tokens
            SET used = 1
            WHERE assumption_id = ?
            """
            cur.execute(update_token_query, (assumption_id,))
            
            conn.commit()
            return {"success": True, "form_id": form_id}
            
        except JWTError:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise self.credentials_exception
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)
            
    def validate_form_data(self, form_data: dict):
        try:
            for key, question_data in form_data.items():
                if key not in ALLOWED_QUESTIONS:
                    raise self.form_exception
                question = question_data.get("question", "")
                question_type = question_data.get("type", "")
                answer = question_data.get("answer", "")
                scale = question_data.get("scale", None)
                
                if question != ALLOWED_QUESTIONS[key]["question"]:
                    raise self.form_exception
                if (question_type != ALLOWED_QUESTIONS[key]["type"]):
                    raise self.form_exception
                if (scale and scale != ALLOWED_QUESTIONS[key].get("scale", None)):
                    raise self.form_exception
                
                if question_type == "scale":
                    self._validate_scale_answer(answer, scale)
                elif question_type == "yes_no_explain":
                    self._validate_yes_no_explain_answer(answer)
        except ValueError or HTTPException:
            raise self.form_exception
             
    def _validate_scale_answer(self, answer: int, scale: list[int]):
        try:
            answer = int(answer)
        except ValueError:
            raise ValueError(f"Answer {answer} is not a valid integer")
        if not scale or len(scale) != 2:
            raise ValueError("Scale must be a list of two integers [min, max]")
        min_val, max_val = scale
        if not (min_val <= answer <= max_val):
            raise ValueError(f"Answer {answer} is out of scale range [{min_val}, {max_val}]")
        
    def _validate_yes_no_explain_answer(self, answer: str):
        if answer not in ["yes", "no"]:
            raise ValueError(f"Answer {answer} is not valid for yes/no question")
