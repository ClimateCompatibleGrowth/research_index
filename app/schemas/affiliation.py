from pydantic import BaseModel
from typing import List, Optional
from .author import AuthorBase

class AffiliationModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    ror: Optional[str] = None
    ccg_partner: Optional[bool] = None
