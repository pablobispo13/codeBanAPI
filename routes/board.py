from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.board import Board, Column
from models.project import Project
from services.auth_service import get_authenticated_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/board", tags=["Board"])
security = HTTPBearer()

class ColumnData(BaseModel):
    name: str
    status: str

class BoardCreateUpdate(BaseModel):
    name: str
    columns: List[ColumnData]

@router.get("/{project_id}/")
def list_boards(project_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    project = Project.objects(id=project_id, createdBy=user).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    # Verifica se o projeto tem um board associado
    if not project.board:
        raise HTTPException(status_code=404, detail="Este projeto não possui um board")

    board = project.board

    return {
        "id": str(board.id),
        "name": board.name,
        "columns": [{"name": c.name, "status": c.status} for c in board.columns]
    }
  
@router.post("/{project_id}/")
def create_board(
    project_id: str,
    board_data: BoardCreateUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = get_authenticated_user(credentials)
    project = Project.objects(id=project_id, createdBy=user).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    # Verifica se o projeto já possui um board
    if project.board:
        raise HTTPException(status_code=400, detail="Este projeto já possui um board")

    # Colunas padrão para o board
    default_columns = [
        Column(name="To Do", status="To Do"),
        Column(name="In Progress", status="In Progress"),
        Column(name="Done", status="Done")
    ]

    # Criação do board com as colunas padrão
    board = Board(
        project=project,
        name=board_data.name,
        columns=default_columns
    )
    board.save()

    # Associa o board ao projeto
    project.board = board
    project.save()

    return {"success": True, "message": "Quadro Kanban criado com sucesso com as colunas padrão", "data": {"id": str(board.id)}}

@router.post("/{board_id}/update")
def update_board(
    board_id: str,
    board_data: BoardCreateUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = get_authenticated_user(credentials)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Encontrar o projeto que foi criado pelo usuário
    project = Project.objects(createdBy=user).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    # Agora, encontre o board relacionado a esse projeto
    board = Board.objects(id=board_id, project=project).first()

    if not board:
        raise HTTPException(status_code=404, detail="Board não encontrado")

    board.name = board_data.name
    board.save()
 
    # Atualiza as colunas do board
    board.columns = [Column(name=column.name, status=column.status) for column in board_data.columns]
    board.save()
    
    return {
        "success": True,
        "message": "Board atualizado com sucesso",
        "data": {
            "id": str(board.id),
            "name": board.name,
            "columns": [{"name": c.name, "status": c.status} for c in board.columns]
        }
    }
