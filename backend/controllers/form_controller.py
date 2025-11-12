from fastapi import APIRouter, status

from services.assumptions_service import AssumptionsService
from fastapi import HTTPException

router = APIRouter(prefix="/form", tags=["Form"])
assumptions_service = AssumptionsService()

# Endpoint for testing purposes that returns fixed assumptions
@router.get("/assumptions/{assumption_id}", status_code=status.HTTP_200_OK)
async def get_assumptions(assumption_id: int):
    pass
    