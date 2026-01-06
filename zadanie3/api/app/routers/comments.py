from __future__ import annotations
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import get_comment, get_task
from ..hateoas import comment_links, comments_list_links
from ..models import Comment, Task
from ..schemas import CommentCreate, CommentListOut, CommentOut



router = APIRouter(
    prefix="/projects/{project_id}/tasks/{task_id}/comments", tags=["comments"]
)




def to_comment_out(project_id: int, task_id: int, c: Comment) -> CommentOut:
    return CommentOut(
        id=c.id,
        task_id=c.task_id,
        content=c.content,
        created_at=c.created_at,
        _links=comment_links(project_id, task_id, c.id),
    )




@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    project_id: int,
    task_id: int,
    payload: CommentCreate,
    response: Response,
    db: Session = Depends(get_db),
    task: Task = Depends(get_task),  
):
    comment = Comment(task_id=task_id, content=payload.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    response.headers[
        "Location"
    ] = f"/projects/{project_id}/tasks/{task_id}/comments/{comment.id}"
    return to_comment_out(project_id, task_id, comment)




@router.get("", response_model=CommentListOut)
def list_comments(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    task: Task = Depends(get_task),
):
    comments = db.scalars(
        select(Comment).where(Comment.task_id == task_id).order_by(Comment.id)
    ).all()

    return CommentListOut(
        items=[to_comment_out(project_id, task_id, c) for c in comments],
        _links=comments_list_links(project_id, task_id),
    )




@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    project_id: int,
    task_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    comment: Comment = Depends(get_comment),
):
    db.delete(comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
