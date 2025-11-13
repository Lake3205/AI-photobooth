from fastapi import APIRouter, UploadFile, status, HTTPException

from services.assumptions_service import AssumptionsService
from services.test_service import TestService
from constants.clients import Clients
from models.assumptions import AssumptionsModel
from constants.model_version_constants import GEMINI_MODEL_VERSION, CLAUDE_MODEL_VERSION

router = APIRouter(prefix="/assumptions", tags=["AI assumptions"])
assumptions_service = AssumptionsService()

@router.post("/generate", status_code=status.HTTP_200_OK)
async def generate_assumptions(image: UploadFile, ai_model: Clients):
    if (ai_model not in Clients):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid AI model specified.")

    assumptions_model = AssumptionsModel()

    match ai_model:
        case Clients.CLAUDE:
            assumptions_model.model = ai_model
            assumptions_model.version = CLAUDE_MODEL_VERSION
        case Clients.GEMINI:
            assumptions_model.model = ai_model
            assumptions_model.version = GEMINI_MODEL_VERSION
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI model not supported yet.")

    assumptions = await assumptions_service.get_assumptions(assumptions_model, image)

    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()

@router.get("/assumptions/{assumption_id}", status_code=status.HTTP_200_OK)
async def get_assumptions(assumption_id: int):
    return await assumptions_service.get_assumptions_by_id(assumption_id)
    

# Endpoint for testing purposes that returns fixed assumptions
@router.post("/test/generate", status_code=status.HTTP_200_OK)
async def generate_test_assumptions():
    assumptions_model = AssumptionsModel()

    assumptions = TestService.generate_assumptions()

    assumptions_model.model = "test_model"
    assumptions_model.version = "1.0"
    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()