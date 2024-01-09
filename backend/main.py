import models
from database import engine
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import document, image, user
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

app_router = APIRouter(prefix="/api")

app_router.include_router(user.router)
#app.include_router(document.router)
#app.include_router(image.router)

app.include_router(app_router)
