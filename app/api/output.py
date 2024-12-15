from fastapi import APIRouter, HTTPException

from app.crud.output import Output
from app.schemas.output import OutputListModel, OutputModel

router = APIRouter(prefix="/api/outputs", tags=["outputs"])


@router.get("")
def api_output_list(
    skip: int = 0, limit: int = 20, type: str = "publication", country: str = None
) -> OutputListModel:
    """Return a list of outputs"""
    if skip < 0:
        raise HTTPException(
            status_code=400, detail="Skip parameter must be non-negative"
        )
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit parameter must be positive")

    outputs = Output()
    try:
        return outputs.get_outputs(skip, limit, type, country)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{id}")
def api_output(id: str) -> OutputModel:
    output = Output()
    try:
        result = output.get_output(id)
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"Output with id {id} not found"
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
