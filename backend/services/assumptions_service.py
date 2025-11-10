from clients.claude import ClaudeClient
from models.assumptions import AssumptionsModel
from constants.clients import Clients
from services.database_service import log_assumption_to_db

from clients.google_ai_client import GoogleAIClient

class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
        self.google_client = GoogleAIClient()

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
                assumption_id = log_assumption_to_db(ai_model=model_name, data=response)
                response['id'] = assumption_id
            except Exception as e:
                print(f"failed to log assumption to database: {e}")

        return response