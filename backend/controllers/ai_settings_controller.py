from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from services.ai_settings_service import AISettingsService
from controllers.auth_controller import get_current_user

router = APIRouter(
    prefix="/api/ai-settings",
    tags=["AI Settings"]
)

ai_settings_service = AISettingsService()


class AISettingUpdate(BaseModel):
    enabled: Optional[bool] = None
    model_version: Optional[str] = None


class AISettingResponse(BaseModel):
    provider: str
    enabled: bool
    model_version: str


@router.get("/", response_model=List[AISettingResponse])
async def get_all_ai_settings(current_user: dict = Depends(get_current_user)):
    """
    Get all AI provider settings (admin only).
    Requires authentication.
    """
    settings = ai_settings_service.get_all_settings()
    return settings


@router.get("/{provider}", response_model=AISettingResponse)
async def get_ai_setting(provider: str, current_user: dict = Depends(get_current_user)):
    """
    Get settings for a specific AI provider (admin only).
    Requires authentication.
    """
    setting = ai_settings_service.get_setting(provider)
    
    if not setting:
        raise HTTPException(status_code=404, detail=f"AI provider '{provider}' not found")
    
    return setting


@router.patch("/{provider}")
async def update_ai_setting(
    provider: str,
    update: AISettingUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update settings for a specific AI provider (admin only).
    Can update enabled status and/or model version.
    Requires authentication.
    """
    # Check if provider exists
    existing = ai_settings_service.get_setting(provider)
    if not existing:
        raise HTTPException(status_code=404, detail=f"AI provider '{provider}' not found")
    
    # Update the setting
    success = ai_settings_service.update_setting(
        provider=provider,
        enabled=update.enabled,
        model_version=update.model_version
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update AI setting")
    
    # Return updated setting
    updated_setting = ai_settings_service.get_setting(provider)
    return updated_setting


@router.get("/providers/enabled", response_model=List[str])
async def get_enabled_providers():
    """
    Get list of enabled AI providers (public endpoint).
    This can be used by the frontend to know which providers are available.
    """
    providers = ai_settings_service.get_enabled_providers()
    return providers
