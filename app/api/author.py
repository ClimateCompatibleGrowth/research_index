from fastapi import APIRouter, HTTPException

from app.crud.author import Author
from app.schemas.author import AuthorListModel, AuthorOutputModel

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.get("")
def api_author_list(skip: int = 0, limit: int = 20) -> AuthorListModel:
    model = Author()
    authors = model.get_all(skip=skip, limit=limit)
    count = model.count_authors()
    return {"meta": {"count": {"total": count}}, "authors": authors}


@router.get("/{id}")
def get_author(id: str, type: str = None) -> AuthorOutputModel:
    author_model = Author()
    results = author_model.get(id, result_type=type)

    if not results:
        raise HTTPException(status_code=404, detail=f"Author with id {id} not found")

    count = author_model.count(id)
    results["outputs"]["meta"] = {
        "count": count,
        "db_response_time_ms": 0,
        "page": 0,
        "per_page": 0,
    }
    return results
