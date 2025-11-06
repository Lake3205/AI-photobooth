from fastapi import APIRouter, status, HTTPException

from services.database_service import get_db_connection, get_assumptions_by_model

router = APIRouter(prefix="/database")

@router.get("/test", status_code=status.HTTP_200_OK)
async def test_database_connection():
    try:
        conn = get_db_connection()
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

@router.get("/assumptions/{ai_model}", status_code=status.HTTP_200_OK)
async def get_assumptions_by_model_endpoint(ai_model: str):
    try:
        result = get_assumptions_by_model(ai_model)
        if result is None:
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
