from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_default_user, engine
from .models import BaseTable
from .routers.api_router import app_router
from .settings import settings

app = FastAPI(title="Markdown TODO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BaseTable.metadata.create_all(bind=engine)

create_default_user()

# App router
app.include_router(app_router)
