from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import get_project, get_user
from ..hateoas import member_links, members_list_links
from ..models import Project, ProjectMember, User
from ..schemas import AddMemberIn, MemberListOut, MemberOut



router = APIRouter(prefix="/projects/{project_id}/members", tags=["members"])




def to_member_out(project_id: int, user: User) -> MemberOut:
    return MemberOut(
        user_id=user.id,
        name=user.name,
        email=user.email,
        _links=member_links(project_id, user.id),
    )




@router.post("", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def add_member(
    project_id: int,
    payload: AddMemberIn,
    response: Response,
    db: Session = Depends(get_db),
    project: Project = Depends(get_project),  
):
    user = get_user(payload.user_id, db)  

    membership = ProjectMember(project_id=project_id, user_id=user.id)
    db.add(membership)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return Response(
            content='{"detail":"User is already a member of this project"}',
            media_type="application/json",
            status_code=status.HTTP_409_CONFLICT,
        )

    response.headers["Location"] = f"/projects/{project_id}/members/{user.id}"
    return to_member_out(project_id, user)




@router.get("", response_model=MemberListOut)
def list_members(
    project_id: int,
    db: Session = Depends(get_db),
    project: Project = Depends(get_project),  
):
    rows = db.execute(
        select(User)
        .join(ProjectMember, ProjectMember.user_id == User.id)
        .where(ProjectMember.project_id == project_id)
        .order_by(User.id)
    ).scalars().all()

    return MemberListOut(
        items=[to_member_out(project_id, u) for u in rows],
        _links=members_list_links(project_id),
    )




@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    project: Project = Depends(get_project),  
):
    membership = db.get(ProjectMember, {"project_id": project_id, "user_id": user_id})
    if not membership:
        return Response(
            content='{"detail":"Member not found in this project"}',
            media_type="application/json",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    db.delete(membership)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
