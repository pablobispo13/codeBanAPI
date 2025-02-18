# Models
from models.user import User

# Imports
import os
import mongoengine as me
from fastapi import FastAPI
from dotenv import load_dotenv
import hashlib
import bcrypt
from pydantic import BaseModel
import pyotp
import jwt
import os
from fastapi.middleware.cors import CORSMiddleware

# Env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

# Connect to mongoDB
me.connect(db="codeBan",host=MONGO_URI)

# Inicializar FastAPI
app = FastAPI(
    title="CodeBan",
    version="0.4"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Types
class UserModel(BaseModel):
    name: str
    email: str
    password: str

class TOTPValidation(BaseModel):
    email: str
    totp_code: str
    
class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str = None

# Resposta para o registro
class RegisterResponse(BaseModel):
    success: bool
    message: str
    qr_code_url: str = None

# Resposta para validação de TOTP
class TOTPValidationResponse(BaseModel):
    success: bool
    message: str
    token: str = None
    
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register",response_model=RegisterResponse)
def register(user_data: UserModel):
    try:
        # Verificar se o e-mail já está cadastrado
        if User.objects(email=user_data.email).first():
            return {"success":False, "message": "E-mail já cadastrado"}

        # Hash da password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), salt)

        # Gerar segredo TOTP
        totp_secret = pyotp.random_base32()

        # Criar usuário no MongoDB
        usuario = User(
            name=user_data.name,
            email=user_data.email,
            pass_hash=hashed_password.decode("utf-8"),
            totp_secret=totp_secret
        )
        usuario.save()

        # Criar URI do OTP
        otp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
            name=user_data.email, issuer_name="CodeBan"
        )

        return {"success":True, "message":"Usuário registrado com sucesso!", "qr_code_url":otp_uri}
    except Exception as e:
        return {"success":False, "message": f"Erro no registro do usuário: {e}"} 

@app.post("/login",response_model=LoginResponse)
def login(user_data: UserModel):
    try:
        # Verificar se o usuário existe
        usuario = User.objects(email=user_data.email).first()
        if not usuario:
             return {"success":False, "message": "E-Usuário não encontrado"}

        # Comparar password com bcrypt
        if not bcrypt.checkpw(user_data.password.encode("utf-8"), usuario.pass_hash.encode("utf-8")):
           return {"success":False, "message": "password incorreta"}

        # Retornar mensagem para validar o código TOTP
        return {"success":True, "message": "Digite o código do Google Authenticator"}
    except Exception as e:
        return {"success":False, "message": f"Erro no login: {e}"} 

@app.post("/totp",response_model=TOTPValidationResponse)
def validate_totp(data: TOTPValidation):
    try:
        usuario = User.objects(email=data.email).first()
        if not usuario:
            return {"success":False, "message": "Usuário não encontrado"}

        # Validar código TOTP
        totp = pyotp.TOTP(usuario.totp_secret)
        if not totp.verify(data.totp_code):
            return {"success":False, "message": "Código TOTP inválido"}

        # Gerar Token JWT
        token = jwt.encode({"email": usuario.email}, SECRET_KEY, algorithm="HS256")

        return {"success":True, "message": "Login bem-sucedido!", "token": token}
    except Exception as e:
        return {"success":False, "message": f"Erro na validação de totp: {e}"} 