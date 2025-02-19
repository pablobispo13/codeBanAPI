from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import User
from services.auth_service import verify_jwt_token

router = APIRouter(prefix="/user", tags=["User"])
security = HTTPBearer()

# Rota protegida para buscar informações do usuário autenticado
@router.get("/info")
def get_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    user = User.objects(email=payload["email"]).first()
    if not user:
        return {"success": False, "message": "Usuário não encontrado", "data": None}

    return {"success": True, "message": "Usuário encontrado", "data": {"name": user.name, "email": user.email}}
