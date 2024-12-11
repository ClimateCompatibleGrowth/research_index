from fastapi import APIRouter, HTTPException
from app.crud.output import Output
from app.schemas.output import OutputModel, OutputListModel

router = APIRouter(
    prefix="/api/outputs",
    tags=["outputs"]
)

@router.get("", response_model=OutputListModel)
def api_output_list(skip: int = 0,
                    limit: int = 20,
                    type: str = 'publication',
                    country: str = None) -> OutputListModel:
    """Return a list of outputs"""
    if skip < 0:
        raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit parameter must be positive")

    model = Output()
    try:
        if country:
            results = model.filter_country(result_type=type,
                                         skip=skip,
                                         limit=limit,
                                         country=country)
        else:
            results = model.filter_type(result_type=type,
                                      skip=skip,
                                      limit=limit)

        count = model.count()

        return {
            "meta": {"count": count,
                    "db_response_time_ms": 0,
                    "page": 0,
                    "per_page": 0},
            "results": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/{id}", response_model=OutputModel)
def api_output(id: str) -> OutputModel:
    output_model = Output()
    try:
        result = output_model.get(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Output with id {id} not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e