from __future__ import annotations
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field





Links = Dict[str, Dict[str, Any]]  # np. {"self": {"href": "...", "method": "GET"}}


# ---------- Projects ----------
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    planned_end_date: Optional[date] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    planned_end_date: Optional[date] = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    planned_end_date: Optional[date]
    _links: Links


class ProjectListOut(BaseModel):
    items: List[ProjectOut]
    _links: Links






# ---------- Tasks ----------
class TaskCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field(default="MEDIUM", max_length=20)
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(default=None, max_length=20)
    due_date: Optional[date] = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    description: Optional[str]
    priority: str
    due_date: Optional[date]
    _links: Links


class TaskListOut(BaseModel):
    items: List[TaskOut]
    _links: Links





# ---------- Users ----------
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    _links: Links


class UserListOut(BaseModel):
    items: List[UserOut]
    _links: Links





# ---------- Members ----------
class AddMemberIn(BaseModel):
    user_id: int


class MemberOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    _links: Links


class MemberListOut(BaseModel):
    items: List[MemberOut]
    _links: Links






# ---------- Comments ----------
class CommentCreate(BaseModel):
    content: str = Field(min_length=1)



class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    content: str
    created_at: datetime
    _links: Links



class CommentListOut(BaseModel):
    items: List[CommentOut]
    _links: Links
