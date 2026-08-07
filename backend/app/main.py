from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.departments import router as departments_router
from app.routes.clubs import router as clubs_router
from app.routes.courses import router as courses_router

app = FastAPI(title="NoticeBoard")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(departments_router)
app.include_router(clubs_router)
app.include_router(courses_router)


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to noticeboard"}
