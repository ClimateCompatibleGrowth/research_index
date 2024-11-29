from pydantic import BaseModel
from typing import List, Optional
from .author import AuthorBase

class WorkstreamModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    members: Optional[List[AuthorBase]] = None
