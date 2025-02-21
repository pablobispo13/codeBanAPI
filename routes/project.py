from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.project import Project
from pydantic import BaseModel
from services.auth_service import get_authenticated_user
from typing import List

router = APIRouter(prefix="/project", tags=["Project"])
security = HTTPBearer()

class ProjectCreateUpdate(BaseModel):
    name: str
    description: str

@router.post("/")
def create_project(
    project_data: ProjectCreateUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = get_authenticated_user(credentials)

    project = Project(
        name=project_data.name,
        description=project_data.description,
        createdBy=user
    )
    project.save()

    return {"success": True, "message": "Projeto criado com sucesso", "data": {"id": str(project.id)}}

@router.post("/{project_id}/update")
def update_project(
    project_id: str,
    project_data: ProjectCreateUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = get_authenticated_user(credentials)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    project = Project.objects(id=project_id, createdBy=user).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    project.name = project_data.name
    project.description = project_data.description
    project.save()

    return {
        "success": True,
        "message": "Projeto atualizado com sucesso",
        "data": {
            "id": str(project.id),
            "name": project.name,
            "description": project.description
        }
    }
    
@router.get("/", response_model=List[dict])
def list_projects(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    projects = Project.objects(createdBy=user)
    
    return [{"id": str(p.id), "name": p.name, "description": p.description} for p in projects]


@router.get("/{project_id}")
def get_project(project_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    project = Project.objects(id=project_id, createdBy=user).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    return {"id": str(project.id), "name": project.name, "description": project.description}

@router.delete("/{project_id}")
def delete_project(project_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_authenticated_user(credentials)
    project = Project.objects(id=project_id, createdBy=user).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    project.delete()
    return {"success": True, "message": "Projeto excluído com sucesso"}