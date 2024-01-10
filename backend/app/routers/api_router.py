from app.routers import document, image, user
from fastapi import APIRouter

app_router = APIRouter(prefix="/api", tags=['api'])

app_router.include_router(user.router)
app_router.include_router(document.router)
app_router.include_router(image.router)
