from fastapi import APIRouter, HTTPException

from app.crud.country import Country
from app.schemas.country import CountryList, CountryOutputListModel

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("")
def api_country_list(skip: int = 0,
                     limit: int = 20
                     ) -> CountryList:
    try:
        country_model = Country()
        return country_model.get_countries(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Server error: {str(e)}") from e

@router.get("/{id}")
def api_country(id: str,
                skip: int = 0,
                limit: int = 20,
                result_type: str = "publication"
                ) -> CountryOutputListModel:
    try:
        country_model = Country()
        if result := country_model.get_country(id, skip, limit, result_type):
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Country with id {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e