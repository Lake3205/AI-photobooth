from fastapi import APIRouter, UploadFile, status, HTTPException

from services.assumptions_service import AssumptionsService
from services.test_service import TestService
from services.form_service import FormService
from constants.clients import Clients
from models.assumptions import AssumptionsModel
from constants.model_version_constants import GEMINI_MODEL_VERSION, CLAUDE_MODEL_VERSION

router = APIRouter(prefix="/assumptions", tags=["AI assumptions"])
assumptions_service = AssumptionsService()
form_service = FormService()

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
            pass
        case Clients.OPENAI:
            assumptions_model.model = ai_model
            assumptions_model.version = "gpt-4o"
            pass
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI model not supported yet.")

    assumptions = await assumptions_service.get_assumptions(assumptions_model, image)

    if ('id' in assumptions and type(assumptions['id'] is int)):
        assumption_id = assumptions['id']
        token = form_service.log_form_token(assumption_id)

        assumptions_model.set_token(token)

    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()

# Endpoint for testing purposes that returns fixed assumptions
@router.post("/test/generate", status_code=status.HTTP_200_OK)
async def generate_test_assumptions():
    assumptions_model = AssumptionsModel()

    assumptions = TestService.generate_assumptions()

    assumptions_model.model = "test_model"
    assumptions_model.version = "1.0"
    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()