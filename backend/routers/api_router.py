from fastapi import APIRouter
from routers import auth, document, image

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(document.router)
api_router.include_router(image.router)
