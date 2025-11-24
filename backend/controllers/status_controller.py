from fastapi import APIRouter, status

from services.status_service import StatusService
from constants.clients import Clients

router = APIRouter(prefix="/status", tags=["Status"])
status_service = StatusService()

# Endpoint for testing purposes that returns fixed assumptions
@router.post("/ai", status_code=status.HTTP_200_OK)
async def check_ai_status(model: Clients):
    status = status_service.check_status(model)
    return status
    