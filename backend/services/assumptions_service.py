from copy import deepcopy

from clients.claude import ClaudeClient
from clients.google_ai_client import GoogleAIClient
from clients.openai_client import OpenAIClient
from constants.clients import Clients
from constants.model_version_constants import GEMINI_MODEL_VERSION, CLAUDE_MODEL_VERSION, OPENAI_MODEL_VERSION
from fastapi import HTTPException
from fastapi import status
from models.assumptions import AssumptionsModel
from services.database_service import DatabaseService


class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
        self.google_client = GoogleAIClient()
        self.db_service = DatabaseService()
        self.openai_client = OpenAIClient()

    async def get_assumptions(self, assumptions_model: AssumptionsModel, image_bytes, mime_type, image_name,
                              detect_face=True) -> dict:
        if detect_face:
            face_detected = await self.google_client.detect_face(image_bytes=image_bytes, mime_type=mime_type)
            if not face_detected.face_detected:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No face detected")

        thought = None
        match assumptions_model.model:
            case Clients.CLAUDE:
                response = await self.claude_client.generate_response(image_bytes, mime_type)
                model_name = "claude"
            case Clients.OPENAI:
                response = await self.openai_client.generate_openai_response(
                    image_bytes,
                    filename=image_name,
                    content_type=mime_type,
                    version=assumptions_model.version
                )
                model_name = "openai"
            case Clients.GEMINI:
                response, thought = await self.google_client.call_gemini_api(
                    image_bytes=image_bytes,
                    mime_type=mime_type
                )
                if response is not None:
                    response = response.to_dict()
                else:
                    response = {}
                model_name = "gemini"
            case _:
                response = {}
                model_name = "unknown"

        # Log the assumption to the database
        if response:
            try:
                assumption_id = self.db_service.log_assumption_to_db(ai_model=model_name, data=response,
                                                                     thought=thought)
                response['id'] = assumption_id
            except Exception as e:
                print(f"failed to log assumption to database: {e}")

        return response

    async def get_thought_by_id(self, assumption_id: int) -> str:
        conn = None
        cur = None

        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()

            query = "SELECT thought FROM assumptions WHERE id = ?"
            cur.execute(query, (assumption_id,))
            row = cur.fetchone()

            if not row:
                return None

            return row[0]

        except Exception as e:
            print(f"Error getting thought: {e}")
            return None
        finally:
            self.db_service.close_resources(cur, conn)

    async def get_assumptions_by_id(self, assumption_id: int) -> dict:
        conn = None
        cur = None

        try:
            conn = self.db_service.get_db_connection()
            cur = conn.cursor()

            assumptions_model = AssumptionsModel()

            query = """
                    SELECT ac.id, ac.value, av.value, av.reasoning
                    FROM assumptions a
                             LEFT JOIN assumption_values av ON a.id = av.assumption_id
                             LEFT JOIN assumption_constants ac ON av.assumption_constant_id = ac.id
                    WHERE a.id = ? \
                    """

            cur.execute(query, (assumption_id,))
            rows = cur.fetchall()

            if not rows:
                raise Exception(f"No assumption found with ID: {assumption_id}")

            for row in rows:
                assumption = row[1]
                value = row[2]
                reasoning = row[3]
                if (assumption in assumptions_model.assumptions):
                    assumptions_model.assumptions[assumption]["value"] = value
                    assumptions_model.assumptions[assumption]["reasoning"] = reasoning

            return assumptions_model.assumptions

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception as rollback_error:
                    print(f"Error during rollback: {rollback_error}")
            raise
        finally:
            self.db_service.close_resources(cur, conn)

    async def compare_assumptions(self, image_bytes, mime_type, image_name, assumptions_id, assumptions_model) -> dict:
        # Get existing assumptions from database (includes thought)
        existing_assumptions_dict = await self.get_assumptions_by_id(assumptions_id)
        existing_thought = await self.get_thought_by_id(assumptions_id)

        detect_face = False
        comparison_results = {
            assumptions_model.model.value.lower(): {
                "thought": existing_thought,
                "assumptions": existing_assumptions_dict
            }
        }

        def change_model(new_assumptions_model: AssumptionsModel, client: Clients, version: str) -> AssumptionsModel:
            current_model = deepcopy(new_assumptions_model)
            current_model.model = client
            current_model.version = version
            return current_model

        def wrap_assumptions(raw_response: dict, thought: str = None) -> dict:
            """Convert raw AI response to structured format with thought and assumptions"""
            assumptions_model_temp = AssumptionsModel()
            for key, value in raw_response.items():
                if key in assumptions_model_temp.assumptions and isinstance(value, dict):
                    assumptions_model_temp.assumptions[key]["value"] = value.get("value")
                    if "reasoning" in value:
                        assumptions_model_temp.assumptions[key]["reasoning"] = value.get("reasoning")
            return {
                "thought": thought,
                "assumptions": assumptions_model_temp.assumptions
            }

        match assumptions_model.model:
            case Clients.CLAUDE:
                gemini_response = await self.get_assumptions(
                    change_model(assumptions_model, Clients.GEMINI, GEMINI_MODEL_VERSION), image_bytes, mime_type,
                    image_name, detect_face
                )
                gemini_thought = await self.get_thought_by_id(gemini_response.get('id')) if gemini_response.get(
                    'id') else None
                comparison_results["gemini"] = wrap_assumptions(gemini_response, gemini_thought)

                openai_response = await self.get_assumptions(
                    change_model(assumptions_model, Clients.OPENAI, OPENAI_MODEL_VERSION), image_bytes, mime_type,
                    image_name, detect_face
                )
                openai_thought = await self.get_thought_by_id(openai_response.get('id')) if openai_response.get(
                    'id') else None
                comparison_results["openai"] = wrap_assumptions(openai_response, openai_thought)

            case Clients.OPENAI:
                claude_response = await self.get_assumptions(
                    change_model(assumptions_model, Clients.CLAUDE, CLAUDE_MODEL_VERSION), image_bytes, mime_type,
                    image_name, detect_face
                )
                claude_thought = await self.get_thought_by_id(claude_response.get('id')) if claude_response.get(
                    'id') else None
                comparison_results["claude"] = wrap_assumptions(claude_response, claude_thought)

                gemini_response = await self.get_assumptions(
                    change_model(assumptions_model, Clients.GEMINI, GEMINI_MODEL_VERSION), image_bytes, mime_type,
                    image_name, detect_face
                )
                gemini_thought = await self.get_thought_by_id(gemini_response.get('id')) if gemini_response.get(
                    'id') else None
                comparison_results["gemini"] = wrap_assumptions(gemini_response, gemini_thought)

            case Clients.GEMINI:
                claude_response = await self.get_assumptions(
                    change_model(assumptions_model, Clients.CLAUDE, CLAUDE_MODEL_VERSION), image_bytes, mime_type,
                    image_name, detect_face
                )
                claude_thought = await self.get_thought_by_id(claude_response.get('id')) if claude_response.get(
                    'id') else None
                comparison_results["claude"] = wrap_assumptions(claude_response, claude_thought)

                openai_response = await self.get_assumptions(
                    change_model(assumptions_model, Clients.OPENAI, OPENAI_MODEL_VERSION), image_bytes, mime_type,
                    image_name, detect_face
                )
                openai_thought = await self.get_thought_by_id(openai_response.get('id')) if openai_response.get(
                    'id') else None
                comparison_results["openai"] = wrap_assumptions(openai_response, openai_thought)

        return comparison_results
