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
    raise NotImplementedError("Implementation of workstream and author relationships is not yet complete")
