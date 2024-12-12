from typing import List

from fastapi import APIRouter, HTTPException

from app.crud.country import Country
from app.schemas.country import CountryNodeModel

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("")
def api_country_list() -> List[CountryNodeModel]:
    try:
        country_model = Country()
        if results := country_model.get_all():
            return [result["c"] for result in results]
        else:
            raise HTTPException(status_code=404, detail="No countries found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
