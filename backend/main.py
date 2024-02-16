from typing import Annotated

import models
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api_router
from services.database import engine
from services.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(api_router.api_router)
