from clients.claude import ClaudeClient
from models.assumptions import AssumptionsModel
from constants.clients import Clients

class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
    
    async def get_assumptions(self, assumptions_model: AssumptionsModel, image) -> dict:
        

        match assumptions_model.model:
            case Clients.CLAUDE:
                response = await self.claude_client.generate_response(image, version=assumptions_model.version)
            case _:
                response = {}
        
        return response
        