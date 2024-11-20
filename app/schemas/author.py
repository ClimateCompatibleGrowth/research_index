from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class AuthorModel(BaseModel):
    """
    Data model representing an academic author or contributor
    with their associated metadata and relationships.
    """

    uuid: str = Field(..., description="Unique identifier for the author")
    orcid: Optional[str] = Field(None, description="Author's ORCID identifier")
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    affiliations: Optional[Dict[str, str]] = None
    workstreams: Optional[Dict[str, str]] = None
    collaborators: Optional[List[str]] = None
    outputs: Optional[List[str]] = None
