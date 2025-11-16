from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserLogin, Token
from services.auth_service import verify_password, create_access_token, verify_token
from services.database_service import DatabaseService

router = APIRouter(prefix="/api/auth", tags=["Auth"])
security = HTTPBearer()
db_service = DatabaseService()

# Login endpoint
@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    user = db_service.get_user_by_username(user_login.username)
    
    if not user or not verify_password(user_login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user from token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_data = verify_token(token)
    
    user = db_service.get_user_by_username(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# Dependency to require admin role
async def require_admin(user = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

# Verify endpoint
@router.get("/verify")
async def verify_auth(user = Depends(get_current_user)):
    return {"username": user["username"], "role": user.get("role", "admin"), "authenticated": True}
