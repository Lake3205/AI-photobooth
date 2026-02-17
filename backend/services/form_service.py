
from services.auth_service import create_access_token
from datetime import timedelta, datetime, timezone
from services.database_service import DatabaseService
from fastapi import HTTPException, status
from jose import JWTError, jwt
from models.assumptions import AssumptionsModel
import config  # Load environment configuration

from constants.form_constants import ALLOWED_QUESTIONS

class FormService:
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.expiration_time = timedelta(days=1)
        self.secret_key = config.JWT_SECRET_KEY
        self.algorithm = config.ALGORITHM
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self.form_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid form data",
        )

    def _get_or_create_question_type(self, cur, question_type: str, scale: list[int] | None = None):
        cur.execute(
            """
            SELECT id, min, max FROM form_question_types
            WHERE value = ?
            """,
            (question_type,)
        )
        result = cur.fetchone()

        min_val = scale[0] if question_type == "scale" and scale and len(scale) > 0 else None
        max_val = scale[1] if question_type == "scale" and scale and len(scale) > 1 else None

        if result:
            question_type_id = result[0]
            if question_type == "scale" and (result[1] != min_val or result[2] != max_val):
                cur.execute(
                    """
                    UPDATE form_question_types
                    SET min = ?, max = ?
                    WHERE id = ?
                    """,
                    (min_val, max_val, question_type_id)
                )
            return question_type_id

        cur.execute(
            """
            INSERT INTO form_question_types (value, min, max)
            VALUES (?, ?, ?)
            """,
            (question_type, min_val, max_val)
        )
        return cur.lastrowid

    def _ensure_default_questions(self, cur):
        cur.execute("SELECT COUNT(*) FROM form_questions")
        result = cur.fetchone()
        question_count = result[0] if result else 0

        if question_count > 0:
            return

        for question_data in ALLOWED_QUESTIONS.values():
            question_text = question_data.get("question", "")
            question_type = question_data.get("type", "")
            scale = question_data.get("scale", None)

            question_type_id = self._get_or_create_question_type(cur, question_type, scale)
            cur.execute(
                """
                INSERT INTO form_questions (question_type_id, question)
                VALUES (?, ?)
                """,
                (question_type_id, question_text)
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
        
    def log_form_token(self, assumption_id: int, session_id: int = None):
        conn = None
        cur = None
        
        access_token = self.create_form_token(assumption_id)
        expires_at = datetime.now(timezone.utc) + self.expiration_time
        
        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()
            
            query = """
            INSERT INTO form_tokens (token, assumption_id, expires_at, session_id)
            VALUES (?, ?, ?, ?)
            """
            
            cur.execute(query, (access_token, assumption_id, expires_at, session_id))
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
            SELECT ac.id, ac.value, av.value, av.reasoning, a.thought
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

            thought = None
            for row in result:
                (id, assumption, value, reasoning, row_thought) = row
                if thought is None:
                    thought = row_thought
                if (assumption in assumptions_model.assumptions):
                    assumptions_model.assumptions[assumption]["value"] = value
                    assumptions_model.assumptions[assumption]["reasoning"] = reasoning

            return {
                "thought": thought,
                "assumptions": assumptions_model.assumptions
            }
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
                if not question_key.startswith("q_"):
                    raise self.form_exception

                try:
                    question_id = int(question_key[2:])
                except ValueError:
                    raise self.form_exception

                question_metadata_query = """
                SELECT fq.id, fq.question, fqt.value, fqt.min, fqt.max
                FROM form_questions fq
                JOIN form_question_types fqt ON fq.question_type_id = fqt.id
                WHERE fq.id = ?
                """
                cur.execute(question_metadata_query, (question_id,))
                metadata_result = cur.fetchone()

                if not metadata_result:
                    raise self.form_exception

                question_text = question_data.get("question", "")
                question_type = question_data.get("type", "")
                answer = question_data.get("answer", "")
                explanation = question_data.get("explanation", "")
                scale = question_data.get("scale", None)

                expected_question_text = metadata_result[1]
                expected_question_type = metadata_result[2]
                expected_scale = [metadata_result[3], metadata_result[4]] if metadata_result[3] is not None and metadata_result[4] is not None else None

                if question_text != expected_question_text:
                    raise self.form_exception
                if question_type != expected_question_type:
                    raise self.form_exception

                if question_type == "scale":
                    if expected_scale is None or scale != expected_scale:
                        raise self.form_exception
                    self._validate_scale_answer(answer, expected_scale)
                elif question_type == "yes_no_explain":
                    self._validate_yes_no_explain_answer(answer)
                else:
                    raise self.form_exception
                
                insert_result_query = """
                INSERT INTO form_results (form_id, form_question_id, value, explanation)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(insert_result_query, (form_id, question_id, answer, explanation if explanation else None))
            
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
            allowed_questions = self.get_form_questions()

            for key, question_data in form_data.items():
                if key not in allowed_questions:
                    raise self.form_exception
                question = question_data.get("question", "")
                question_type = question_data.get("type", "")
                answer = question_data.get("answer", "")
                scale = question_data.get("scale", None)
                
                if question != allowed_questions[key]["question"]:
                    raise self.form_exception
                if (question_type != allowed_questions[key]["type"]):
                    raise self.form_exception
                if (scale and scale != allowed_questions[key].get("scale", None)):
                    raise self.form_exception
                
                if question_type == "scale":
                    allowed_scale = allowed_questions[key].get("scale", None)
                    if not allowed_scale:
                        raise self.form_exception
                    self._validate_scale_answer(answer, allowed_scale)
                elif question_type == "yes_no_explain":
                    self._validate_yes_no_explain_answer(answer)
        except (ValueError, HTTPException):
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

    def get_form_questions(self):
        conn = None
        cur = None

        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()

            self._ensure_default_questions(cur)

            query = """
            SELECT fq.id, fq.question, fqt.value, fqt.min, fqt.max
            FROM form_questions fq
            JOIN form_question_types fqt ON fq.question_type_id = fqt.id
            ORDER BY fq.id
            """
            cur.execute(query)
            rows = cur.fetchall()
            conn.commit()

            questions = {}
            for row in rows:
                question_id = row[0]
                question_text = row[1]
                question_type = row[2]
                min_val = row[3]
                max_val = row[4]

                question_key = f"q_{question_id}"
                questions[question_key] = {
                    "question": question_text,
                    "type": question_type,
                }

                if question_type == "scale" and min_val is not None and max_val is not None:
                    questions[question_key]["scale"] = [int(min_val), int(max_val)]

            return questions
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)

    def add_form_question(self, question_data: dict):
        conn = None
        cur = None

        try:
            question_text = question_data.get("question", "").strip()
            question_type = question_data.get("type", "")
            scale = question_data.get("scale", None)

            if not question_text:
                raise self.form_exception
            if question_type not in ["scale", "yes_no_explain"]:
                raise self.form_exception
            if question_type == "scale":
                if not isinstance(scale, list) or len(scale) != 2:
                    raise self.form_exception
                self._validate_scale_answer(scale[0], scale)
                self._validate_scale_answer(scale[1], scale)
            if question_type == "yes_no_explain":
                scale = None

            conn = self.db_service.get_db_connection()
            cur = conn.cursor()

            question_type_id = self._get_or_create_question_type(cur, question_type, scale)
            cur.execute(
                """
                INSERT INTO form_questions (question_type_id, question)
                VALUES (?, ?)
                """,
                (question_type_id, question_text)
            )

            question_id = cur.lastrowid
            conn.commit()

            response = {
                "id": question_id,
                "key": f"q_{question_id}",
                "question": question_text,
                "type": question_type,
            }
            if question_type == "scale" and scale:
                response["scale"] = scale

            return response
        except HTTPException:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise self.form_exception
        finally:
            self.db_service.close_resources(cur, conn)

    def delete_form_question(self, question_id: int):
        conn = None
        cur = None

        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()

            cur.execute(
                """
                DELETE FROM form_questions
                WHERE id = ?
                """,
                (question_id,)
            )

            if cur.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

            conn.commit()
            return {"success": True, "deleted_id": question_id}
        except HTTPException:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)

    def get_form_results(self):
        conn = None
        cur = None

        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()

            query = """
            SELECT 
                fq.id,
                fq.question,
                fqt.value as question_type,
                fqt.min,
                fqt.max,
                fr.value,
                fr.explanation
            FROM form_questions fq
            JOIN form_question_types fqt ON fq.question_type_id = fqt.id
            LEFT JOIN form_results fr ON fq.id = fr.form_question_id
            ORDER BY fq.id, fr.id
            """
            cur.execute(query)
            rows = cur.fetchall()

            # Group results by question
            questions_map = {}
            for row in rows:
                question_id = row[0]
                question_text = row[1]
                question_type = row[2]
                min_val = row[3]
                max_val = row[4]
                answer_value = row[5]
                explanation = row[6]

                if question_id not in questions_map:
                    questions_map[question_id] = {
                        "id": question_id,
                        "question": question_text,
                        "type": question_type,
                        "answers": []
                    }
                    
                    if question_type == "scale" and min_val is not None and max_val is not None:
                        questions_map[question_id]["scale"] = [int(min_val), int(max_val)]

                # Only add answer if it exists (LEFT JOIN might return NULL)
                if answer_value is not None:
                    answer_entry = {"value": answer_value}
                    if explanation:
                        answer_entry["explanation"] = explanation
                    questions_map[question_id]["answers"].append(answer_entry)

            return list(questions_map.values())
        except Exception:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)