from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

from . import AuthorBase
from .workstream import WorkstreamBase
from .affiliation import AffiliationModel
from .output import OutputListModel
from .meta import Meta


class AuthorListModel(AuthorBase):
    """
    Data model representing an academic author or contributor
    with their associated metadata and relationships.
    """
    affiliations: Optional[List[AffiliationModel]] = None
    workstreams: Optional[List[WorkstreamBase]] = None


class AuthorModel(AuthorListModel):
    collaborators: List[AuthorBase] = None
    outputs: OutputListModel
