from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import get_user
from ..hateoas import user_links, users_list_links
from ..models import User
from ..schemas import UserCreate, UserListOut, UserOut



router = APIRouter(prefix="/users", tags=["users"])



def to_user_out(u: User) -> UserOut:
    return UserOut(
        id=u.id,
        name=u.name,
        email=u.email,
        _links=user_links(u.id),
    )



@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    user = User(name=payload.name, email=str(payload.email))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        return Response(
            content='{"detail":"User with this email already exists"}',
            media_type="application/json",
            status_code=status.HTTP_409_CONFLICT,
        )

    db.refresh(user)
    response.headers["Location"] = f"/users/{user.id}"
    return to_user_out(user)



@router.get("", response_model=UserListOut)
def list_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User).order_by(User.id)).all()
    return UserListOut(
        items=[to_user_out(u) for u in users],
        _links=users_list_links(),
    )



@router.get("/{user_id}", response_model=UserOut)
def get_user_details(user: User = Depends(get_user)):
    return to_user_out(user)



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: User = Depends(get_user), db: Session = Depends(get_db)):
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
