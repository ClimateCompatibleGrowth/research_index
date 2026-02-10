from pydantic import BaseModel

from . import WorkstreamBase
from .author import AuthorListModel
from .meta import MetaAuthor
from .output import OutputListModel


class WorkstreamDetailModel(WorkstreamBase):
    members: AuthorListModel


class WorkstreamListModel(BaseModel):
    meta: MetaAuthor
    results: list[WorkstreamBase]
