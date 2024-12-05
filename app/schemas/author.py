from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

from . import AuthorBase
from .workstream import WorkstreamBase
from .affiliation import AffiliationModel
from .output import OutputListModel


class AuthorModel(AuthorBase):
    """
    Data model representing an academic author or contributor
    with their associated metadata and relationships.
    """
    affiliations: Optional[List[AffiliationModel]] = None
    workstreams: Optional[List[WorkstreamBase]] = None
    collaborators: List[AuthorBase] = None
    outputs: OutputListModel
