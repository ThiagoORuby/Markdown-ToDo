from fastapi import APIRouter
from routers import document, image, user

app_router = APIRouter(prefix="/api", tags=['api'])

app_router.include_router(user.router)
app_router.include_router(document.router)
app_router.include_router(image.router)
