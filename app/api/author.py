from fastapi import APIRouter, HTTPException, Query, Path
from typing import Annotated
from uuid import UUID

from app.crud.author import Author
from app.schemas.author import AuthorListModel, AuthorOutputModel
from app.schemas.query import FilterWorkstream, FilterParams

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.get("")
def api_author_list(query: Annotated[FilterWorkstream, Query()]
                    ) -> AuthorListModel:
    try:
        authors = Author()
        if result := authors.get_authors(skip=query.skip,
                                         limit=query.limit,
                                         workstream=query.workstream):
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

@router.get("/{id}")
def api_author(id: Annotated[UUID, Path(title="Unique author identifier")],
               query: Annotated[FilterParams, Query()]
               ) -> AuthorOutputModel:
    try:
        author = Author()
        if result := author.get_author(id=id,
                                       result_type=query.result_type,
                                       skip=query.skip,
                                       limit=query.limit):
            return result
        else:
            raise HTTPException(status_code=404,
                                detail=f"Author '{id}' not found")
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail=f"Database error: {str(e)}") from e
