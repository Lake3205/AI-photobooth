from constants.assumptions_constants import (
    EDUCATION_LEVELS, GENERATIONS, MARITAL_STATUSES, FORMAT_TYPES
)

from clients.claude import ClaudeClient
from models.assumptions import AssumptionsModel

class AssumptionsService:
    def __init__(self):
        self.claude_client = ClaudeClient()
    
    async def get_assumptions(self, assumptions_model: AssumptionsModel, image) -> dict:
        

        match assumptions_model.model:
            case "claude":
                response = await self.claude_client.generate_response(image, version=assumptions_model.version)
            case _:
                response = {}
        
        return response
        