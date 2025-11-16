from fastapi import APIRouter, status, HTTPException, Depends

from services.database_service import DatabaseService
from controllers.auth_controller import get_current_user, require_admin

router = APIRouter(prefix="/database", tags=["Database"])
db_service = DatabaseService()

# Endpoint to test database connection
@router.get("/test", status_code=status.HTTP_200_OK)
async def test_database_connection():
    try:
        conn = db_service.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            return {
                "status": "success",
                "message": "Database connection successful",
                "result": result[0]
            }
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

# Endpoint to get assumptions by AI model, with user authentication
@router.get("/assumptions/{ai_model}", status_code=status.HTTP_200_OK)
async def get_assumptions_by_model_endpoint(ai_model: str, user = Depends(require_admin)): # Require admin role
    try:
        result = db_service.get_assumptions_by_model(ai_model)
        if result is None or len(result) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No assumptions found for model: {ai_model}"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve assumptions: {str(e)}"
        )

# Endpoint to get all assumptions
@router.get("/assumptions", status_code=status.HTTP_200_OK)
async def get_all_assumptions_endpoint(user = Depends(require_admin)):
    try:
        result = db_service.get_all_assumptions()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve assumptions: {str(e)}"
        )

# Endpoint to get all assumption constants
@router.get("/constants", status_code=status.HTTP_200_OK)
async def get_assumption_constants_endpoint(user = Depends(require_admin)):
    try:
        result = db_service.get_assumption_constants()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve assumption constants: {str(e)}"
        )

# Endpoint to get all formats
@router.get("/formats", status_code=status.HTTP_200_OK)
async def get_formats_endpoint(user = Depends(require_admin)):
    try:
        result = db_service.get_formats()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve formats: {str(e)}"
        )

# Endpoint to delete an assumption
@router.delete("/assumptions/{assumption_id}", status_code=status.HTTP_200_OK)
async def delete_assumption_endpoint(assumption_id: int, user = Depends(require_admin)):
    try:
        result = db_service.delete_assumption(assumption_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete assumption: {str(e)}"
        )
