import jwt
import bcrypt
import pyotp
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from models.user import User
from datetime import datetime, timedelta
from fastapi.security import  HTTPAuthorizationCredentials

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_jwt_token(email: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=48)
    payload = {
        "email": email,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"success": False, "message": "Token expirado", "data": None})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"success": False, "message": "Token inválido", "data": None})

def validate_totp_code(email: str, code: str) -> bool:
    user = User.objects(email=email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"success": False, "message": "Usuário não encontrado", "data": None})

    totp = pyotp.TOTP(user.totp_secret)
    return totp.verify(code)

def get_authenticated_user(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    user = User.objects(email=payload["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user