from fastapi import APIRouter, UploadFile, File

from services.assumptions_service import AssumptionsService

router = APIRouter(prefix="/assumptions")
assumptions_service = AssumptionsService()

@router.get("")
def get_assumptions():
    return assumptions_service.get_assumptions()

@router.post("/generate")
def generate_assumptions(image: UploadFile = File(...)):
    assumptions = assumptions_service.get_assumptions()
    return {image.filename: assumptions}