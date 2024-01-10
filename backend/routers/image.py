from typing import Optional

from daos import DocumentDao, ImageDao
from database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import User
from schemas import DocumentIn, DocumentOut, ImageIn, ImageOut
from services import DocumentService, UserService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/image", tags=['image'])


@router.get("", status_code=status.HTTP_200_OK)
async def get_images(doc_id: int,
                     current_user: User = Depends(
                         UserService.get_current_user),
                     session: Session = Depends(get_session)):

    await DocumentService.validate_document(doc_id, current_user.id, session)

    results = ImageDao(session).get_by_doc_id(doc_id)

    images = [ImageOut.model_validate(result) for result in results]

    return {"images": images}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_image(doc_id: int,
                       data: ImageIn,
                       current_user: User = Depends(
                           UserService.get_current_user),
                       session: Session = Depends(get_session)):

    await DocumentService.validate_document(doc_id, current_user.id, session)

    data.doc_id = doc_id
    _image = ImageDao(session).create(data)

    return ImageOut.model_validate(_image)


@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
async def delete_image(image_id: int,
                       doc_id: int,
                       current_user: User = Depends(
                           UserService.get_current_user),
                       session: Session = Depends(get_session)):

    await DocumentService.validate_document(doc_id, current_user.id, session)

    _image = ImageDao(session).get_by_id(image_id)

    if not _image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image not found")

    ImageDao(session).delete_by_id(image_id)

    return {"message": "Image deleted successfully"}
