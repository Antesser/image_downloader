from fastapi import FastAPI

from file_loader.router import router as file_uploader

app = FastAPI(title="Test task")

app.include_router(file_uploader)
