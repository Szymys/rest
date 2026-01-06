from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_project
from ..hateoas import project_links, projects_list_links
from ..models import Project
from ..schemas import ProjectCreate, ProjectListOut, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])





def to_project_out(p: Project) -> ProjectOut:
    return ProjectOut(
        id=p.id,
        name=p.name,
        description=p.description,
        start_date=p.start_date,
        planned_end_date=p.planned_end_date,
        _links=project_links(p.id),
    )




@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    project = Project(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
        planned_end_date=payload.planned_end_date,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    response.headers["Location"] = f"/projects/{project.id}"
    return to_project_out(project)


@router.get("", response_model=ProjectListOut)
def list_projects(db: Session = Depends(get_db)):
    projects = db.scalars(select(Project).order_by(Project.id)).all()
    return ProjectListOut(
        items=[to_project_out(p) for p in projects],
        _links=projects_list_links(),
    )


@router.get("/{project_id}", response_model=ProjectOut)
def get_project_details(project: Project = Depends(get_project)):
    return to_project_out(project)




@router.put("/{project_id}", response_model=ProjectOut)
def replace_project(
    payload: ProjectCreate,
    project: Project = Depends(get_project),
    db: Session = Depends(get_db),
):
    
    project.name = payload.name
    project.description = payload.description
    project.start_date = payload.start_date
    project.planned_end_date = payload.planned_end_date

    db.commit()
    db.refresh(project)
    return to_project_out(project)




@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
    payload: ProjectUpdate,
    project: Project = Depends(get_project),
    db: Session = Depends(get_db),
):
    
    for field in payload.model_fields_set:
        setattr(project, field, getattr(payload, field))

    db.commit()
    db.refresh(project)
    return to_project_out(project)




@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project: Project = Depends(get_project),
    db: Session = Depends(get_db),
):
    db.delete(project)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
