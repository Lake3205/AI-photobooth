from fastapi import APIRouter

from backend.services.assumptions_sevice import AssumptionsService

router = APIRouter(prefix="/assumptions")
assumptions_service = AssumptionsService()

@router.get("")
def get_assumptions():
    return assumptions_service.get_assumptions()
