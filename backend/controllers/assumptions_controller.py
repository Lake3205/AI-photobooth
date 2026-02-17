from anthropic import AuthenticationError, RateLimitError, APIError
from constants.clients import Clients
from constants.model_version_constants import GEMINI_MODEL_VERSION, CLAUDE_MODEL_VERSION, OPENAI_MODEL_VERSION
from fastapi import APIRouter, status, HTTPException
from fastapi import UploadFile
from google.genai import errors
from models.assumptions import AssumptionsModel
from openai import AuthenticationError, RateLimitError
from services.assumptions_service import AssumptionsService
from services.form_service import FormService
from services.test_service import TestService

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
    if ai_model not in Clients:
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
    
    # Create a session for this selfie request
    session_id = assumptions_service.db_service.create_assumption_session(image_name, mime_type)

    try:
        assumptions = await assumptions_service.get_assumptions(assumptions_model, image_bytes, mime_type, image_name,
                                                                detect_face, session_id)
    except errors.ClientError as e:
        if e.code == 429:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                detail="Gemini rate limit exceeded") from e
        if e.code == 400 and "API key not valid" in e.message:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Gemini API key") from e
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gemini API error") from e
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
        if hasattr(e, 'message'):
            detail = str(e.message)
        else:
            detail = str(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail) from e

    if 'id' in assumptions and type(assumptions['id'] is int):
        assumption_id = assumptions['id']
        token = form_service.log_form_token(assumption_id, session_id)

        assumptions_model.set_token(token)
        assumptions_model.assumption_id = assumption_id

    assumptions_model.set_assumptions_json(assumptions)

    return assumptions_model.to_dict()


@router.post("/generate-all", status_code=status.HTTP_200_OK)
async def generate_all_assumptions(image: UploadFile):
    """Generate assumptions from all available AI models (Gemini, OpenAI, Claude) in one session"""
    image_bytes, mime_type, image_name = read_image_bytes(image)
    
    # Create ONE session for all AI models
    session_id = assumptions_service.db_service.create_assumption_session(image_name, mime_type)
    
    # Disable face detection for all models in batch generation (assumed to be pre-checked)
    detect_face = False
    results = {
        "session_id": session_id,
        "assumptions": {}
    }
    
    # Try Gemini
    try:
        gemini_model = AssumptionsModel()
        gemini_model.model = Clients.GEMINI
        gemini_model.version = GEMINI_MODEL_VERSION
        
        gemini_assumptions = await assumptions_service.get_assumptions(
            gemini_model, image_bytes, mime_type, image_name, detect_face, session_id
        )
        
        if 'id' in gemini_assumptions:
            gemini_model.assumption_id = gemini_assumptions['id']
            token = form_service.log_form_token(gemini_assumptions['id'], session_id)
            gemini_model.set_token(token)
        
        gemini_model.set_assumptions_json(gemini_assumptions)
        gemini_dict = gemini_model.to_dict()
        # Add thought to the response for comparison view
        if 'thought' in gemini_assumptions:
            gemini_dict['thought'] = gemini_assumptions['thought']
        results["assumptions"]["gemini"] = gemini_dict
        results["primary_token"] = gemini_model.token  # Use Gemini's token as primary
        
    except Exception as e:
        results["assumptions"]["gemini"] = {"error": str(e)}
    
    # Try OpenAI
    try:
        openai_model = AssumptionsModel()
        openai_model.model = Clients.OPENAI
        openai_model.version = OPENAI_MODEL_VERSION
        
        openai_assumptions = await assumptions_service.get_assumptions(
            openai_model, image_bytes, mime_type, image_name, False, session_id
        )
        
        if 'id' in openai_assumptions:
            openai_model.assumption_id = openai_assumptions['id']
        
        openai_model.set_assumptions_json(openai_assumptions)
        openai_dict = openai_model.to_dict()
        # Add thought to the response for comparison view
        if 'thought' in openai_assumptions:
            openai_dict['thought'] = openai_assumptions['thought']
        results["assumptions"]["openai"] = openai_dict
        
    except Exception as e:
        results["assumptions"]["openai"] = {"error": str(e)}
    
    # Try Claude (skip if no API key)
    if assumptions_service.claude_client.api_key:
        try:
            claude_model = AssumptionsModel()
            claude_model.model = Clients.CLAUDE
            claude_model.version = CLAUDE_MODEL_VERSION
            
            claude_assumptions = await assumptions_service.get_assumptions(
                claude_model, image_bytes, mime_type, image_name, False, session_id
            )
            
            if 'id' in claude_assumptions:
                claude_model.assumption_id = claude_assumptions['id']
            
            claude_model.set_assumptions_json(claude_assumptions)
            claude_dict = claude_model.to_dict()
            # Add thought to the response for comparison view
            if 'thought' in claude_assumptions:
                claude_dict['thought'] = claude_assumptions['thought']
            results["assumptions"]["claude"] = claude_dict
            
        except Exception as e:
            results["assumptions"]["claude"] = {"error": str(e)}
    
    return results


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
    comparison_results = await assumptions_service.compare_assumptions(image_bytes, mime_type, image_name,
                                                                       assumptions_id, assumptions_model)
    return comparison_results
