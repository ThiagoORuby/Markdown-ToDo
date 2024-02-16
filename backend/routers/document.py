from typing import Annotated, Optional

from daos.document import DocumentDao
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models import User
from schemas import DocumentIn, DocumentOut
from services.database import get_session
from services.service import AuthService, DocumentService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=DocumentOut)
async def create_document(
        document: DocumentIn,
        current_user: Annotated[User,
                                Depends(AuthService.get_current_user)],
        session: Annotated[Session, Depends(get_session)]):

    _doc = DocumentDao(session).create(document, current_user.id)

    return DocumentOut.model_validate(_doc)


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=list[DocumentOut])
async def read_documents(query: Optional[str] = None,
                         current_user: User = Depends(
                             AuthService.get_current_user),
                         session: Session = Depends(get_session)):

    if query:
        results = DocumentDao(session).get_by_query(query, current_user.id)
    else:
        results = DocumentDao(session).get_by_user_id(current_user.id)

    _docs = [DocumentOut.model_validate(_doc) for _doc in results]

    return _docs


@router.put("/{doc_id}", status_code=status.HTTP_200_OK)
async def update_document(
        doc_id: str, document: DocumentIn,
        current_user: Annotated[User,
                                Depends(AuthService.get_current_user)],
        session: Annotated[Session, Depends(get_session)]):

    _doc = await DocumentService.validate_document(doc_id, current_user.id,
                                                   session)

    DocumentDao(session).update(_doc, document)

    return JSONResponse(content={"message": "Documento atualizado"},
                        status_code=status.HTTP_200_OK)


@router.delete("/{doc_id}", status_code=status.HTTP_200_OK)
async def delete_document(
        doc_id: str,
        current_user: Annotated[User,
                                Depends(AuthService.get_current_user)],
        session: Annotated[Session, Depends(get_session)]):

    _doc = await DocumentService.validate_document(doc_id, current_user.id,
                                                   session)

    DocumentDao(session).delete_by_id(_doc.id)

    return JSONResponse(content={"message": "Documento deletado"},
                        status_code=status.HTTP_200_OK)
