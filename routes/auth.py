from fastapi import APIRouter
from models.user import User
from services.auth_service import (
    hash_password,
    verify_password,
    create_jwt_token,
    validate_totp_code
)
from pydantic import BaseModel
import pyotp

router = APIRouter(prefix="/auth", tags=["Auth"])

# Modelos de entrada
class UserModel(BaseModel):
    email: str
    password: str

class TOTPValidation(BaseModel):
    email: str
    totp_code: str

# Rota de Registro
@router.post("/register")
def register(user_data: UserModel):
    if User.objects(email=user_data.email).first():
        return {"success": False, "message": "E-mail já cadastrado", "data": None}

    hashed_password = hash_password(user_data.password)
    totp_secret = pyotp.random_base32()

    new_user = User(name=user_data.name, email=user_data.email, pass_hash=hashed_password, totp_secret=totp_secret)
    new_user.save()

    otp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=user_data.email, issuer_name="CodeBan")

    return {"success": True, "message": "Usuário registrado com sucesso!", "data": {"qr_code_url": otp_uri}}

# Rota de Login
@router.post("/login")
def login(user_data: UserModel):
    user = User.objects(email=user_data.email).first()
    if not user or not verify_password(user_data.password, user.pass_hash):
        return {"success": False, "message": "Usuário ou senha incorretos", "data": None}

    return {"success": True, "message": "Digite o código do Google Authenticator", "data": None}

# Rota de Validação de TOTP
@router.post("/totp")
def validate_totp(data: TOTPValidation):
    if not validate_totp_code(data.email, data.totp_code):
        return {"success": False, "message": "Código TOTP inválido", "data": None}

    token = create_jwt_token(data.email)
    return {"success": True, "message": "Login bem-sucedido!", "data": {"token": token}}
