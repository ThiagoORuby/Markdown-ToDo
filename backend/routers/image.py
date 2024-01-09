from typing import Optional

from daos import DocumentDao
from database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import User
from schemas import DocumentIn, DocumentOut
from services import UserService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/image", tags=['image'])
