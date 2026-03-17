from fastapi import FastAPI
from .database import engine, Base
from .routes import experiments
from app.routes import copilot
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(
    experiments.router,
    prefix="/experiments",
    tags=["Experiments"]
)

app.include_router(copilot.router, tags=["Copilot"])

