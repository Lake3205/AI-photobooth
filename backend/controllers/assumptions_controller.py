from fastapi import APIRouter

from services.assumptions_service import AssumptionsService

router = APIRouter(prefix="/assumptions")
assumptions_service = AssumptionsService()

@router.get("")
def get_assumptions():
    return assumptions_service.get_assumptions()
