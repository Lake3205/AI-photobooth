from clients.claude import ClaudeClient
from models.assumptions import AssumptionsModel
from constants.clients import Clients
from services.database_service import DatabaseService

from clients.google_ai_client import GoogleAIClient
from services.form_service import FormService

class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
        self.google_client = GoogleAIClient()
        self.db_service = DatabaseService()
        self.form_service = FormService()

    async def get_assumptions(self, assumptions_model: AssumptionsModel, image) -> dict:
        match assumptions_model.model:
            case Clients.CLAUDE:
                response = await self.claude_client.generate_response(image)
                model_name = "claude"
            case Clients.GEMINI:
                image_bytes = await image.read()
                mime_type = image.content_type
                response = await self.google_client.call_gemini_api(
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
                assumption_id = self.db_service.log_assumption_to_db(ai_model=model_name, data=response)
                self.form_service.log_form_token(assumption_id)
                response['id'] = assumption_id
            except Exception as e:
                print(f"failed to log assumption to database: {e}")

        return response
    
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
            WHERE a.id = ?
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