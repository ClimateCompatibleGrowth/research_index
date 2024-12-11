from typing import List
from fastapi import APIRouter, HTTPException
from app.crud.author import Author 
from app.schemas.author import AuthorModel, AuthorListModel

router = APIRouter(
    prefix="/api/authors",
    tags=["authors"]
)

@router.get("", response_model=List[AuthorListModel])
def list_authors(skip: int = 0, limit: int = 20):
    model = Author()
    return model.get_all(skip=skip, limit=limit)

@router.get("/{id}", response_model=AuthorModel)
def get_author(id: str, type: str = None):
    author_model = Author()
    results = author_model.get(id, result_type=type)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id {id} not found"
        )
        
    count = author_model.count(id)
    results['outputs']['meta'] = {
        "count": count,
        "db_response_time_ms": 0,
        "page": 0,
        "per_page": 0
    }
    return results