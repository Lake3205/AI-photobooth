from fastapi import APIRouter, status, HTTPException

from services.database_service import get_db_connection

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

