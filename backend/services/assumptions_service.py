from clients.claude import ClaudeClient
from models.assumptions import AssumptionsModel

from clients.openai_client import OpenAIClient


class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
        self.openai_client = OpenAIClient()
    
    async def get_assumptions(self, assumptions_model: AssumptionsModel, image) -> dict:
        

        match assumptions_model.model:
            case "claude":
                response = await self.claude_client.generate_response(image, version=assumptions_model.version)
            case "openai":
                response = await self.openai_client.generate_openai_response(image, version=assumptions_model.version)
            case _:
                response = {}
        
        return response
        