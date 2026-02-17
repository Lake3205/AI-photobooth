from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from jose import JWTError

from services.form_service import FormService
from controllers.auth_controller import require_admin

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
        
@router.get("/questions", status_code=status.HTTP_200_OK)
def get_form_questions():
    return form_service.get_form_questions()

@router.get("/results", status_code=status.HTTP_200_OK)
def get_form_results(_user = Depends(require_admin)):
    try:
        return form_service.get_form_results()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch form results",
        )

@router.post("/questions", status_code=status.HTTP_201_CREATED)
def add_form_question(question_data: dict, _user = Depends(require_admin)):
    try:
        return form_service.add_form_question(question_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add question",
        )

@router.delete("/questions/{question_id}", status_code=status.HTTP_200_OK)
def delete_form_question(question_id: int, _user = Depends(require_admin)):
    try:
        return form_service.delete_form_question(question_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete question",
        )
        
@router.post("/submit", status_code=status.HTTP_200_OK)
def submit_form(form_data: dict, token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    try:
        response = form_service.verify_form_token(token.credentials)
        form_service.validate_form_data(form_data)
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
        