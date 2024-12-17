from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from . meta import Pagination
from . output import OutputListModel
from . import CountryBaseModel


class CountryOutputListModel(OutputListModel, CountryBaseModel):
    """Data model representing country outputs"""



class CountryNodeModel(CountryBaseModel):
    dbpedia: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    official_name: Optional[str] = None


class CountryList(BaseModel):

    meta: Pagination
    results: list[CountryNodeModel]
