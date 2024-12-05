from typing import Dict, List
from pydantic import BaseModel, HttpUrl


class DomainModel(BaseModel):
    id: int
    display_name: str


class FieldModel(BaseModel):
    id: int
    display_name: str


class TopicBaseModel(BaseModel):
    id: HttpUrl
    description: str
    display_name: str
    domain: DomainModel
    field: FieldModel
    subfield: FieldModel
    ids: Dict[str, HttpUrl]
    keywords: List[str]
