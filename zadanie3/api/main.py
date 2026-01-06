from fastapi import FastAPI

from app.db import Base, engine
from app.hateoas import root_links
from app.routers.comments import router as comments_router
from app.routers.members import router as members_router
from app.routers.projects import router as projects_router
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router


app = FastAPI(title="Task API", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    
    from app import models  

    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "0.1.0",
        "_links": root_links(),
    }


@app.get("/health")
def health():
    return {"status": "ok"}



app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(members_router)
app.include_router(comments_router)
