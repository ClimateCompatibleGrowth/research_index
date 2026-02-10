from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, Query

from app.crud.workstream import Workstream
from app.schemas.query import FilterBase
from app.schemas.workstream import WorkstreamDetailModel, WorkstreamListModel

router = APIRouter(prefix="/api/workstreams", tags=["workstreams"])


@router.get("")
def list_workstreams(query: Annotated[FilterBase, Query()]) -> WorkstreamListModel:
    """Return a list of workstreams

    Returns
    -------
    app.schemas.workstream.WorkstreamListModel

    """
    model = Workstream()
    try:
        results = model.get_all(skip=query.skip, limit=query.limit)
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
    else:
        return results


@router.get("/{id}")
def get_workstream(
    id: Annotated[str, Path(title="Unique workstream identifier")],
    query: Annotated[FilterBase, Query()],
) -> WorkstreamDetailModel:
    """Return a single workstream"""
    model = Workstream()
    try:
        results = model.get(id, skip=query.skip, limit=query.limit)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Workstream '{id}' not found")
    else:
        return results
