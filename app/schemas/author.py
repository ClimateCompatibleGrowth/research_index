from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    """
    Base data model representing an academic author or contributor
    with their associated metadata.
    """

    uuid: str = Field(..., description="Unique identifier for the author")
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    orcid: Optional[str] = Field(None, description="Author's ORCID identifier")

    
class AuthorModel(AuthorBase):
    """
    Data model representing an academic author or contributor
    with their associated metadata and relationships.
    """
    affiliations: Optional[Dict] = None
    workstreams: Optional[Dict[str, str]] = None
    collaborators: Optional[List] = None
    outputs: Optional[List] = None
