from pydantic import BaseModel
from typing import List, Optional

class WorkstreamModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
