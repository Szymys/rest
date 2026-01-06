from __future__ import annotations

from typing import Any, Dict, Optional

Links = Dict[str, Dict[str, Any]]





def link(href: str, method: str = "GET") -> Dict[str, Any]:
    return {"href": href, "method": method}


def root_links() -> Links:
    return {
        "self": link("/"),
        "health": link("/health"),
        "projects": link("/projects"),
        "users": link("/users"),
    }





# -------- Projects --------
def project_links(project_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}"),
        "collection": link("/projects"),
        "tasks": link(f"/projects/{project_id}/tasks"),
        "members": link(f"/projects/{project_id}/members"),
        "update": link(f"/projects/{project_id}", "PUT"),
        "delete": link(f"/projects/{project_id}", "DELETE"),
    }


def projects_list_links() -> Links:
    return {
        "self": link("/projects"),
        "create": link("/projects", "POST"),
    }





# -------- Tasks --------
def task_links(project_id: int, task_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}/tasks/{task_id}"),
        "project": link(f"/projects/{project_id}"),
        "collection": link(f"/projects/{project_id}/tasks"),
        "comments": link(f"/projects/{project_id}/tasks/{task_id}/comments"),
        "update": link(f"/projects/{project_id}/tasks/{task_id}", "PUT"),
        "delete": link(f"/projects/{project_id}/tasks/{task_id}", "DELETE"),
    }


def tasks_list_links(project_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}/tasks"),
        "create": link(f"/projects/{project_id}/tasks", "POST"),
        "project": link(f"/projects/{project_id}"),
    }





# -------- Users --------
def user_links(user_id: int) -> Links:
    return {
        "self": link(f"/users/{user_id}"),
        "collection": link("/users"),
        "delete": link(f"/users/{user_id}", "DELETE"),  
    }


def users_list_links() -> Links:
    return {
        "self": link("/users"),
        "create": link("/users", "POST"),
    }





# -------- Members --------
def members_list_links(project_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}/members"),
        "add": link(f"/projects/{project_id}/members", "POST"),
        "project": link(f"/projects/{project_id}"),
    }


def member_links(project_id: int, user_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}/members/{user_id}"),
        "project": link(f"/projects/{project_id}"),
        "collection": link(f"/projects/{project_id}/members"),
        "remove": link(f"/projects/{project_id}/members/{user_id}", "DELETE"),
    }





# -------- Comments --------
def comments_list_links(project_id: int, task_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}/tasks/{task_id}/comments"),
        "add": link(f"/projects/{project_id}/tasks/{task_id}/comments", "POST"),
        "task": link(f"/projects/{project_id}/tasks/{task_id}"),
    }


def comment_links(project_id: int, task_id: int, comment_id: int) -> Links:
    return {
        "self": link(f"/projects/{project_id}/tasks/{task_id}/comments/{comment_id}"),
        "collection": link(f"/projects/{project_id}/tasks/{task_id}/comments"),
        "task": link(f"/projects/{project_id}/tasks/{task_id}"),
        "delete": link(
            f"/projects/{project_id}/tasks/{task_id}/comments/{comment_id}", "DELETE"
        ),
    }
