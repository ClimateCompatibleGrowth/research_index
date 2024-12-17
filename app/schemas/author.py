from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

from . import AuthorBase
from .workstream import WorkstreamBase
from .affiliation import AffiliationModel
from .output import OutputListModel
from .meta import MetaAuthor


class AuthorColabModel(AuthorBase):
    """
    An academic author or contributor
    with their collaborators, workstreams and affiliations
    """
    workstreams: List[WorkstreamBase] = None
    affiliations: List[AffiliationModel] = None


class AuthorListModel(BaseModel):
    """
    A list of authors
    """
    authors: List[AuthorColabModel]
    meta: MetaAuthor


class AuthorOutputModel(AuthorColabModel):
    """An author with collaborators, workstreams, affiliations and outputs"""
    collaborators: List[AuthorBase] = None
    outputs: OutputListModel
