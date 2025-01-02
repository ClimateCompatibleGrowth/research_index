from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID


class AuthorBase(BaseModel):
    """
    Base data model representing an academic author or contributor
    with their associated metadata.
    """

    uuid: UUID = Field(...,
                       description="Unique identifier for the author")
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    orcid: Optional[HttpUrl] = \
        Field(None, description="Author's ORCID identifier")


class CountryBaseModel(BaseModel):
    id: str
    name: str
