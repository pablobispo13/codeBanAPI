import os
import mongoengine as me
from fastapi import FastAPI,HTTPException
from dotenv import load_dotenv
from models.project import Project  # Importando o modelo Project
from models.user import User  # Importando o modelo User
from models.task import Task  # Importando o modelo Task

# Carregar variáveis de ambiente
load_dotenv()

# Conectar ao MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
me.connect(db="codeBan",host=MONGO_URI)

# Inicializar FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    me.connect(db="codeBan",host=MONGO_URI)
    try:
        me.connect(db="codeBan",host=MONGO_URI)
        return {"message": "✅ Conectado ao MongoDB com sucesso!"} 
    except Exception as e:
        return {"message": f"❌ Erro ao conectar no MongoDB: {e}"} 

@app.get("/init")
def setup():
    try:
        usuario = User.objects(email="contato.pabloed@email.com").first()
        if not usuario:
            usuario = User(name="Pablo Bispo", email="contato.pabloed@email.com").save()

        projeto = Project.objects(name="codeBan").first()
        if not projeto:
            projeto = Project(name="codeBan", description="Um projeto de kanban de projetos", createdBy=usuario).save()

        tarefa = Task(title="Criar banco de dados e conectar com a api", project=projeto, user=usuario).save()

        return {
            "message": "Setup verificado/criado com sucesso!",
            "usuario": {"id": str(usuario.id), "name": usuario.name, "email": usuario.email},
            "projeto": {"id": str(projeto.id), "name": projeto.name, "description": projeto.description},
            "tarefa": {"id": str(tarefa.id), "title": tarefa.title, "status": tarefa.status},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")