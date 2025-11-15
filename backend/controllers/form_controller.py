from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from jose import JWTError

from services.form_service import FormService

router = APIRouter(prefix="/form", tags=["Form"])
form_service = FormService()
bearer_scheme = HTTPBearer()

@router.get("/token/verify", status_code=status.HTTP_200_OK)
def verify_form_token(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    try:
        response = form_service.verify_form_token(token.credentials)
        if response.get("valid"):
            return {"valid": True}
        return {"valid": False}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid form token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
@router.get("/assumptions", status_code=status.HTTP_200_OK)
def get_assumptions(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    try:
        return form_service.get_assumptions_by_token(token.credentials)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid form token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
@router.post("/submit", status_code=status.HTTP_200_OK)
def submit_form(form_data: dict, token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    try:
        response = form_service.verify_form_token(token.credentials, revoke=True) # TODO change to True when in production
        if not response.get("valid"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid form token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        assumption_id = response.get("assumption_id")
        form_service.submit_form_responses(form_data, assumption_id)
    except JWTError or Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid form token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        