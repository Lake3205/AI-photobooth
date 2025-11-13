from fastapi import APIRouter, status

from services.assumptions_service import AssumptionsService
from fastapi import HTTPException
from services.database_service import DatabaseService

router = APIRouter(prefix="/form", tags=["Form"])
assumptions_service = AssumptionsService()

