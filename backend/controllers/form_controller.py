from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

from services.form_service import FormService


router = APIRouter(prefix="/form", tags=["Form"])
form_service = FormService()
bearer_scheme = HTTPBearer()

@router.get("/token/verify", status_code=status.HTTP_200_OK)
async def verify_form_token(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    try:
        form_service.verify_form_token(token.credentials)
        return {"valid": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid form token",
            headers={"WWW-Authenticate": "Bearer"},
        )