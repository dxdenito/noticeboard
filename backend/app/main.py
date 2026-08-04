from fastapi import FastAPI

from app.routes.health import router as health_router

app = FastAPI(title="NoticeBoard")

app.include_router(health_router)
@app.get("/")
def root()->dict:
    return {"message": "Welcome to noticeboard"}

