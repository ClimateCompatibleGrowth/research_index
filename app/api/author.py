from fastapi import APIRouter, HTTPException

from app.crud.author import Author
from app.schemas.author import AuthorListModel, AuthorOutputModel

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.get("")
def api_author_list(skip: int = 0, limit: int = 20, workstream: str = None) -> AuthorListModel:
    try:
        authors = Author()
        if result := authors.get_authors(skip=skip, limit=limit, workstream=workstream):
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Workstream {workstream} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

@router.get("/{id}")
def api_author(id: str, result_type: str = 'publication', skip: int = 0, limit: int = 20) -> AuthorOutputModel:
    try:
        author = Author()
        if result := author.get_author(id=id, result_type=result_type, skip=skip, limit=limit):
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Author {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
