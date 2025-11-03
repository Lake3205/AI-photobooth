from fastapi import APIRouter, UploadFile, File, status, HTTPException

from services.assumptions_service import AssumptionsService
from clients.clients import CLIENTS
from models.assumptions import AssumptionsModel

router = APIRouter(prefix="/assumptions")
assumptions_service = AssumptionsService()

@router.post("/generate", status_code=status.HTTP_200_OK)
async def generate_assumptions(image: UploadFile, ai_model: str):
    if (ai_model not in CLIENTS):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid AI model specified.")
    
    assumptions_model = AssumptionsModel()
    
    match ai_model:
        case "claude":
            assumptions_model.model = ai_model
            assumptions_model.version = "claude-sonnet-4-5"
            pass
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI model not supported yet.")
        
    assumptions = await assumptions_service.get_assumptions(assumptions_model, image)
        
    assumptions_model.assumptions = assumptions
    
    return assumptions_model.to_dict()
