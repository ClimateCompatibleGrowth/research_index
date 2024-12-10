from pydantic import BaseModel
from typing import List, Optional
from . import AuthorBase
from .output import OutputListModel

class WorkstreamBase(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

class WorkstreamModel(WorkstreamBase):
    members: List[AuthorBase]
    outputs: OutputListModel
