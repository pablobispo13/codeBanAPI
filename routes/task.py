from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.board import Board
from models.task import Task
from services.auth_service import get_authenticated_user
from pydantic import BaseModel

router = APIRouter(prefix="/task", tags=["Task"])
security = HTTPBearer()

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    status: str

@router.post("/{board_id}")
def create_task(
    board_id: str,
    task_data: TaskCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = get_authenticated_user(credentials)
    board = Board.objects(id=board_id, project__createdBy=user).first()

    if not board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")

    task = Task(
        board=board,
        title=task_data.title,
        description=task_data.description
    )
    task.save()

    return {"success": True, "message": "Tarefa criada com sucesso", "data": {"id": str(task.id)}}

@router.get("/{board_id}")
def list_tasks(board_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    board = Board.objects(id=board_id, project__createdBy=user).first()

    if not board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")

    tasks = Task.objects(board=board)

    return [{"id": str(t.id), "title": t.title, "status": t.status} for t in tasks]

@router.post("/{task_id}/update")
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = get_authenticated_user(credentials)
    task = Task.objects(id=task_id, board__project__createdBy=user).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    task.status = task_update.status
    task.save()

    return {"success": True, "message": "Tarefa atualizada com sucesso"}

@router.delete("/{task_id}")
def delete_task(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    task = Task.objects(id=task_id, board__project__createdBy=user).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    task.delete()
    return {"success": True, "message": "Tarefa excluída com sucesso"}