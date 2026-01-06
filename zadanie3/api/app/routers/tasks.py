from __future__ import annotations
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import get_project, get_task
from ..hateoas import task_links, tasks_list_links
from ..models import Project, Task
from ..schemas import TaskCreate, TaskListOut, TaskOut, TaskUpdate


router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])




def to_task_out(t: Task) -> TaskOut:
    return TaskOut(
        id=t.id,
        project_id=t.project_id,
        name=t.name,
        description=t.description,
        priority=t.priority,
        due_date=t.due_date,
        _links=task_links(t.project_id, t.id),
    )




@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    payload: TaskCreate,
    response: Response,
    db: Session = Depends(get_db),
    project: Project = Depends(get_project),  
):
    task = Task(
        project_id=project_id,
        name=payload.name,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    response.headers["Location"] = f"/projects/{project_id}/tasks/{task.id}"
    return to_task_out(task)




@router.get("", response_model=TaskListOut)
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    project: Project = Depends(get_project),  
):
    tasks = db.scalars(
        select(Task).where(Task.project_id == project_id).order_by(Task.id)
    ).all()

    return TaskListOut(
        items=[to_task_out(t) for t in tasks],
        _links=tasks_list_links(project_id),
    )




@router.get("/{task_id}", response_model=TaskOut)
def get_task_details(task: Task = Depends(get_task)):
    return to_task_out(task)




@router.put("/{task_id}", response_model=TaskOut)
def replace_task(
    payload: TaskCreate,
    task: Task = Depends(get_task),
    db: Session = Depends(get_db),
):
    task.name = payload.name
    task.description = payload.description
    task.priority = payload.priority
    task.due_date = payload.due_date

    db.commit()
    db.refresh(task)
    return to_task_out(task)



@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    payload: TaskUpdate,
    task: Task = Depends(get_task),
    db: Session = Depends(get_db),
):
    for field in payload.model_fields_set:
        setattr(task, field, getattr(payload, field))

    db.commit()
    db.refresh(task)
    return to_task_out(task)



@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task: Task = Depends(get_task),
    db: Session = Depends(get_db),
):
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
