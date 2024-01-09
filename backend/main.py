import models
from database import create_default_user, engine
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.api_router import app_router
from settings import settings

app = FastAPI(title="Markdown TODO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.BaseTable.metadata.create_all(bind=engine)

create_default_user()

# App router
app.include_router(app_router)
