from typing import List

from fastapi import APIRouter, HTTPException

from app.crud.workstream import Workstream
from app.schemas.workstream import WorkstreamDetailModel, WorkstreamListModel

router = APIRouter(prefix="/api/workstreams", tags=["workstreams"])


@router.get("")
def list_workstreams(skip: int = 0, limit: int = 20) -> WorkstreamListModel:
    model = Workstream()
    return model.get_all(skip=skip, limit=limit)


@router.get("/{id}")
def get_workstream(id: str, skip: int = 0, limit: int = 20) -> WorkstreamDetailModel:
    model = Workstream()
    return model.get(id, skip=skip, limit=limit)
