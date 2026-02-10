from typing import Optional

from pydantic import BaseModel


class AffiliationModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    ror: Optional[str] = None
    ccg_partner: Optional[bool] = None
