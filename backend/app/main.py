from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.departments import router as departments_router

app = FastAPI(title="NoticeBoard")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(departments_router)


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to noticeboard"}
