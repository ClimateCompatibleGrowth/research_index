"""The topics schema mimics the OpenAlex implementation of topics

See the OpenAlex documentation: https://docs.openalex.org/api-entities/topics/topic-object

"""
from typing import Dict, List
from pydantic import BaseModel, HttpUrl
from uuid import UUID


class DomainModel(BaseModel):
    id: int
    display_name: str


class FieldModel(BaseModel):
    id: int
    display_name: str


class TopicBaseModel(BaseModel):
    """The topics schema mimics the OpenAlex implementation of topics

    See the OpenAlex documentation:
    https://docs.openalex.org/api-entities/topics/topic-object

    """
    id: UUID
    openalex_id: HttpUrl
    description: str
    display_name: str
    domain: DomainModel
    field: FieldModel
    subfield: FieldModel
    ids: Dict[str, HttpUrl]
    keywords: List[str]
