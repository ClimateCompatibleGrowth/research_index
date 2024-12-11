from typing import List
from fastapi import APIRouter, HTTPException
from app.crud.workstream import Workstream 
from app.schemas.workstream import WorkstreamBase, WorkstreamModel

router = APIRouter(
    prefix="/api/workstreams",
    tags=["workstreams"]
)

@router.get("", response_model=List[WorkstreamBase])
def list_workstreams():
    model = Workstream()
    return model.get_all()

@router.get("/{id}", response_model=WorkstreamModel)
def get_workstream(id: str):
    model = Workstream()
    result = model.get(id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Workstream with id {id} not found"
        )
    return result