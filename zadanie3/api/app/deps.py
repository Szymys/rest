from __future__ import annotations

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db
from .models import Comment, Project, Task, User




def get_project(project_id: int, db: Session = Depends(get_db)) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project




def get_task(
    project_id: int, task_id: int, db: Session = Depends(get_db)
) -> Task:
    task = db.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found in this project",
        )
    return task




def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user




def get_comment(
    project_id: int, task_id: int, comment_id: int, db: Session = Depends(get_db)
) -> Comment:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )




    task = db.get(Task, comment.task_id)
    if not task or task.id != task_id or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found for this task/project",
        )
    return comment
