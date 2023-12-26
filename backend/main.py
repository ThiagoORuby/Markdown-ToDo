from fastapi import FastAPI, Depends
from typing import Annotated
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from routers import user, document, image
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
#app.include_router(document.router)
#app.include_router(image.router)

