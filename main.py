from fastapi import FastAPI
from core import router
from fastapi.testclient import TestClient

#entrypoint

app = FastAPI(
    title="Docs",
    summary="A sample application created for implementation of repository pattern using fastapi",
)

app.include_router(router)
