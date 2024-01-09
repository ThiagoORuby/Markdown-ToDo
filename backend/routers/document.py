from typing import Optional

from daos import DocumentDao
from database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import User
from schemas import DocumentIn, DocumentOut
from services import UserService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/document", tags=['document'])


@router.get("", status_code=status.HTTP_200_OK)
async def get_documents(query: Optional[str] = None,
                        current_user: User = Depends(
                            UserService.get_current_user),
                        session: Session = Depends(get_session)):

    if not query:
        results = DocumentDao(session).get_by_user_id(current_user.id)
    else:
        results = DocumentDao(session).get_by_query(query, current_user.id)

    documents = [DocumentOut.model_validate(result) for result in results]

    return {"documents": documents}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_document(data: DocumentIn,
                          current_user: User = Depends(
                              UserService.get_current_user),
                          session: Session = Depends(get_session)):

    data.user_id = current_user.id
    _doc = DocumentDao(session).create(data)

    return DocumentOut.model_validate(_doc)


@router.put("/{doc_id}", status_code=status.HTTP_200_OK)
async def update_document(doc_id: int,
                          data: DocumentIn,
                          current_user: User = Depends(
                              UserService.get_current_user),
                          session: Session = Depends(get_session)):

    _doc = DocumentDao(session).get_by_id(doc_id)

    if not _doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Document not found")

    if _doc.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    _doc = DocumentDao(session).update(_doc, data)

    return DocumentOut.model_validate(_doc)


@router.delete("/{doc_id}")
async def delete_document(doc_id: int,
                          current_user: User = Depends(
                              UserService.get_current_user),
                          session: Session = Depends(get_session)):

    _doc = DocumentDao(session).get_by_id(doc_id)

    if not _doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Document not found")

    if _doc.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    DocumentDao(session).delete_by_id(doc_id)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Document deleted"})
