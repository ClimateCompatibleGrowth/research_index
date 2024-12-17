from fastapi import APIRouter, HTTPException

from app.crud.author import Author
from app.schemas.author import AuthorListModel, AuthorOutputModel

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.get("")
def api_author_list(skip: int = 0, limit: int = 20) -> AuthorListModel:
    authors = Author()
    return authors.get_authors(skip=skip, limit=limit)


@router.get("/{id}")
def api_author(id: str, result_type: str = 'publication', skip: int = 0, limit: int = 20) -> AuthorOutputModel:
    author = Author()
    return author.get_author(id=id, result_type=result_type, skip=skip, limit=limit)
