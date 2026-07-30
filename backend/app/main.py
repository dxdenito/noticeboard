from fastapi import FastAPI

app = FastAPI(title="NoticeBoard")


@app.get("/")
def root():
    return {"message": "Welcome to noticeboard"}
