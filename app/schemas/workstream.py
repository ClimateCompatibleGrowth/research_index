from pydantic import BaseModel
from .output import OutputListModel
from .meta import MetaAuthor
from .author import AuthorListModel
from . import WorkstreamBase


class WorkstreamDetailModel(WorkstreamBase):
    members: AuthorListModel


class WorkstreamListModel(BaseModel):
    meta: MetaAuthor
    results: list[WorkstreamBase]
