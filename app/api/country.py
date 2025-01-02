from fastapi import APIRouter, HTTPException, Query, Path
from typing import Annotated
from app.crud.country import Country
from app.schemas.country import CountryList, CountryOutputListModel
from app.schemas.query import FilterBase, FilterParams

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("")
def api_country_list(query: Annotated[FilterBase, Query()]
                     ) -> CountryList:
    country_model = Country()
    try:
        return country_model.get_countries(query.skip, query.limit)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Server error: {str(e)}") from e

@router.get("/{id}")
def api_country(id: Annotated[str, Path(examples=['KEN'], title="Country identifier", pattern="^([A-Z]{3})$")],
                query: Annotated[FilterParams, Query()]
                ) -> CountryOutputListModel:
    country_model = Country()
    try:
        result = country_model.get_country(id,
                                           query.skip,
                                           query.limit,
                                           query.result_type)
    except KeyError:
        raise HTTPException(status_code=404,
                            detail=f"Country with id {id} not found")
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail=f"Database error: {str(e)}") from e

    else:
        return result
