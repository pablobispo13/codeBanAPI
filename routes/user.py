from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import get_authenticated_user

router = APIRouter(prefix="/user", tags=["User"])
security = HTTPBearer()

@router.get("/profile")
def get_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    if not user:
        return {"success": False, "message": "Usuário não encontrado", "data": None}

    return {"success": True, "message": "Usuário encontrado", "data": {"name": user.name, "email": user.email}}
