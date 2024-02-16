import re
from pathlib import Path

import aiofiles
from daos.image import ImageDao
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from models import User
from schemas import ImageIn, ImageOut
from services.database import get_session
from services.service import AuthService, DocumentService
from services.settings import settings
from sqlalchemy.orm import Session

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(
        doc_id: str,
        data: UploadFile = File(...),
        current_user: User = Depends(AuthService.get_current_user),
        session: Session = Depends(get_session),
):

    filename = Path(
        re.sub(r"[/ ]", "_", data.filename) if data.filename else "unknown")

    if filename.suffix not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="File extension not allowed")

    _path = Path(settings.UPLOADS_PATH) / current_user.id

    _path.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(_path / filename, "wb") as buffer:
        while content := await data.read(1024):  # async read chunk
            await buffer.write(content)

    ImageDao(session).create(
        ImageIn(name=str(filename), url=str(_path / filename)), doc_id)

    return JSONResponse(content={"message": "Image uploaded"},
                        status_code=status.HTTP_201_CREATED)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ImageOut])
async def get_images_ids(
        doc_id: str,
        current_user: User = Depends(AuthService.get_current_user),
        session: Session = Depends(get_session),
):
    await DocumentService.validate_document(doc_id, current_user.id, session)

    results = ImageDao(session).get_by_doc_id(doc_id)

    images = [ImageOut.model_validate(result) for result in results]

    return images


@router.get("/{image_id}",
            status_code=status.HTTP_200_OK,
            response_class=FileResponse)
async def get_image(image_id: str,
                    doc_id: str,
                    current_user: User = Depends(AuthService.get_current_user),
                    session: Session = Depends(get_session)):

    await DocumentService.validate_document(doc_id, current_user.id, session)

    _image = ImageDao(session).get_by_id(image_id)

    if not _image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem nao encontrada",
        )

    _path = Path(_image.url)

    if not _path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem nao encontrada",
        )

    return FileResponse(path=_image.url, filename=_image.name)


@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
async def delete_image(image_id: str,
                       doc_id: str,
                       current_user: User = Depends(
                           AuthService.get_current_user),
                       session: Session = Depends(get_session)):
    await DocumentService.validate_document(doc_id, current_user.id, session)

    _image = ImageDao(session).get_by_id(image_id)

    if not _image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image not found")

    _path = Path(_image.url)

    if _path.is_file():
        _path.unlink()

    ImageDao(session).delete_by_id(image_id)

    return JSONResponse(content={"message": "Image deleted"},
                        status_code=status.HTTP_200_OK)
