from clients.claude import ClaudeClient
from models.assumptions import AssumptionsModel
from constants.clients import Clients

from clients.google_ai_client import GoogleAIClient

class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
        self.google_client = GoogleAIClient()

    async def get_assumptions(self, assumptions_model: AssumptionsModel, image) -> dict:
        match assumptions_model.model:
            case Clients.CLAUDE:
                response = await self.claude_client.generate_response(image)
            case Clients.GEMINI:
                image_bytes = await image.read()
                mime_type = image.content_type
                response = await self.google_client.call_gemini_api(
                    image_bytes=image_bytes,
                    mime_type=mime_type
                )
                response = response.to_dict()
            case _:
                response = {}

        return response