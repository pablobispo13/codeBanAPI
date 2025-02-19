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
from urllib.parse import urlparse, parse_qs

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserRegisterModel(BaseModel):
    name: str
    email: str
    password: str
    
class LoginModel(BaseModel):
    email: str
    password: str

class TOTPValidation(BaseModel):
    email: str
    totp_code: str

@router.post("/register")
def register(user_data: UserRegisterModel):
    if User.objects(email=user_data.email).first():
        return {"success": False, "message": "E-mail já cadastrado", "data": None}

    hashed_password = hash_password(user_data.password)
    totp_secret = pyotp.random_base32()

    new_user = User(name=user_data.name, email=user_data.email, pass_hash=hashed_password, totp_secret=totp_secret)
    new_user.save()

    otp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=user_data.email, issuer_name="CodeBan")
    parsed_uri = urlparse(otp_uri)
    query_params = parse_qs(parsed_uri.query)
    secret_value = query_params.get('secret', [None])[0]
    
    return {"success": True, "message": "Usuário registrado com sucesso!", "data": {"qr_code_url": otp_uri,"qrcode_url_value":secret_value}}

@router.post("/login")
def login(user_data: LoginModel):
    user = User.objects(email=user_data.email).first()
    if not user or not verify_password(user_data.password, user.pass_hash):
        return {"success": False, "message": "Usuário ou senha incorretos", "data": None}

    return {"success": True, "message": "Digite o código do Google Authenticator", "data": None}

@router.post("/totp")
def validate_totp(data: TOTPValidation):
    if not validate_totp_code(data.email, data.totp_code):
        return {"success": False, "message": "Código TOTP inválido", "data": None}

    token = create_jwt_token(data.email)
    return {"success": True, "message": "Login bem-sucedido!", "data": {"token": token}}
