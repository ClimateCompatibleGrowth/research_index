from typing import List

from fastapi import APIRouter, HTTPException

from app.crud.workstream import Workstream
from app.schemas.workstream import WorkstreamBase, WorkstreamModel

router = APIRouter(prefix="/api/workstreams", tags=["workstreams"])


@router.get("")
def list_workstreams() -> List[WorkstreamBase]:
    model = Workstream()
    return model.get_all()


@router.get("/{id}")
def get_workstream(id: str) -> WorkstreamModel:
    model = Workstream()
    result = model.get(id)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Workstream with id {id} not found"
        )
    return result
