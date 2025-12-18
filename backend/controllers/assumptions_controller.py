from typing import Optional

from fastapi import APIRouter, UploadFile, status, HTTPException

from google.genai import errors
from openai import AuthenticationError, RateLimitError
from anthropic import AuthenticationError, RateLimitError, APIError

from services.assumptions_service import AssumptionsService
from services.test_service import TestService
from services.form_service import FormService
from constants.clients import Clients
from models.assumptions import AssumptionsModel
from constants.model_version_constants import GEMINI_MODEL_VERSION, CLAUDE_MODEL_VERSION, OPENAI_MODEL_VERSION
from fastapi import File, Form, UploadFile


router = APIRouter(prefix="/assumptions", tags=["AI assumptions"])
assumptions_service = AssumptionsService()
form_service = FormService()

def read_image_bytes(image) -> tuple[bytes, str, str]:
    image_bytes_read = image.file.read()
    mime_type_read = image.content_type
    image_name_read = image.filename
    return image_bytes_read, mime_type_read, image_name_read

@router.post("/generate", status_code=status.HTTP_200_OK)
async def generate_assumptions(image: UploadFile, ai_model: Clients):
    if (ai_model not in Clients):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid AI model specified.")

    assumptions_model = AssumptionsModel()

    detect_face = True

    match ai_model:
        case Clients.CLAUDE:
            assumptions_model.model = ai_model
            assumptions_model.version = CLAUDE_MODEL_VERSION
        case Clients.GEMINI:
            assumptions_model.model = ai_model
            assumptions_model.version = GEMINI_MODEL_VERSION
            pass
        case Clients.OPENAI:
            assumptions_model.model = ai_model
            assumptions_model.version = OPENAI_MODEL_VERSION
            pass
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI model not supported yet.")
    image_bytes, mime_type, image_name = read_image_bytes(image)
    
    try:
        assumptions = await assumptions_service.get_assumptions(assumptions_model, image_bytes, mime_type, image_name, detect_face)
    except errors.ClientError as e:
        if e.code == 429:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded") from e
        if e.code == 400 and "API key not valid" in e.message:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Gemini API key") from e
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OpenAI API key") from e
    except RateLimitError as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="OpenAI rate limit exceeded") from e
    except AuthenticationError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid Claude API key") from e
    except RateLimitError as e:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail="Claude rate limit exceeded") from e
    except APIError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Claude API error") from e
    except Exception as e:
        if (hasattr(e, 'message')):
            detail = str(e.message)
        else:
            detail = str(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail) from e

    if ('id' in assumptions and type(assumptions['id'] is int)):
        assumption_id = assumptions['id']
        token = form_service.log_form_token(assumption_id)

        assumptions_model.set_token(token)

    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()

# Endpoint for testing purposes that returns fixed assumptions
@router.post("/test/generate", status_code=status.HTTP_200_OK)
async def generate_test_assumptions():
    assumptions_model = AssumptionsModel()

    assumptions = TestService.generate_assumptions()

    assumptions_model.model = "test_model"
    assumptions_model.version = "1.0"
    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()

@router.post("/compare", status_code=status.HTTP_200_OK)
async def compare_assumptions(
        image: UploadFile,
        assumptions_id: int,
        ai_model: Clients
):
    assumptions_model = AssumptionsModel()

    match ai_model:
        case Clients.CLAUDE:
            assumptions_model.model = ai_model
            assumptions_model.version = CLAUDE_MODEL_VERSION
        case Clients.GEMINI:
            assumptions_model.model = ai_model
            assumptions_model.version = GEMINI_MODEL_VERSION
            pass
        case Clients.OPENAI:
            assumptions_model.model = ai_model
            assumptions_model.version = OPENAI_MODEL_VERSION
            pass
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI model not supported yet.")

    image_bytes, mime_type, image_name = read_image_bytes(image)
    comparison_results = await assumptions_service.compare_assumptions(image_bytes, mime_type, image_name, assumptions_id, assumptions_model)
    return comparison_results


