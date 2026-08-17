from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.departments import router as departments_router
from app.routes.clubs import router as clubs_router
from app.routes.courses import router as courses_router
from app.routes.notices import router as notices_router
from app.routes.attachments import router as attachment_router
from app.routes.category import router as category_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.admin.users import router as admin_users_router
from app.routes.roles import router as roles_router


app = FastAPI(title="NoticeBoard")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://10.2.14.26:5173","http://192.168.137.1:5173","http://192.168.0.104:5173"],  # your Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(category_router)
app.include_router(departments_router)
app.include_router(clubs_router)
app.include_router(courses_router)
app.include_router(notices_router)
app.include_router(attachment_router)
app.include_router(admin_users_router)
app.include_router(roles_router)


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to noticeboard"}
