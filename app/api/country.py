from typing import List
from fastapi import APIRouter, HTTPException
from app.crud.country import Country
from app.schemas.country import CountryNodeModel
from app.schemas.output import OutputListModel

router = APIRouter(
    prefix="/api/countries",
    tags=["countries"]
)

@router.get("", response_model=List[CountryNodeModel])
def list_countries():
    model = Country()
    return model.get_all()

# @router.get("/{id}", response_model=OutputListModel)
# def get_country(id: str, type: str = None):
#     model = Country()
#     outputs, country = model.get(id, result_type=type)
    
#     if not country:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Country with id {id} not found"
#         )
        
#     return {"items": outputs}