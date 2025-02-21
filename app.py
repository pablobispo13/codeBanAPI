from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, user, project, board, task
import mongoengine as me
import os

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("A variável de ambiente MONGO_URI não está definida")

me.connect(db="codeBan", host=MONGO_URI)

app = FastAPI(title="CodeBan", version="0.4",debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(board.router)
app.include_router(task.router)

@app.get("/")
def root():
    return {"success": True, "message": "API está rodando!"}
