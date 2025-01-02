from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.logger import logger
from typing import Annotated
from app.schemas.query import FilterOutputList
from uuid import UUID

from app.crud.output import Output
from app.schemas.output import OutputListModel, OutputModel

router = APIRouter(prefix="/api/outputs", tags=["outputs"])


@router.get("")
def api_output_list(
    query: Annotated[FilterOutputList, Query()]
) -> OutputListModel:
    """Return a list of outputs"""
    outputs = Output()
    try:
        return outputs.get_outputs(query.skip,
                                   query.limit,
                                   query.result_type,
                                   query.country)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{id}")
def api_output(id: Annotated[UUID, Path(title="Unique output identifier")]) -> OutputModel:
    output = Output()
    try:
        result = output.get_output(id)
    except KeyError:
        raise HTTPException(
                status_code=404, detail=f"Output with id {id} not found"
            )
    except Exception as e:
        logger.error(f"Error in api_output: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    else:
        return result
