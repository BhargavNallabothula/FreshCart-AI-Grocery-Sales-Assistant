from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers.chat_controller import chat_router

app = FastAPI(title="FreshCart AI Grocery Sales Assistant")

app.include_router(chat_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")
