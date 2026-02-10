from typing import List, Literal

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class FilterBase(BaseModel):
    skip: int = Field(
        default=0, ge=0, title="Skip", description="Number of records to skip"
    )
    limit: int = Field(
        default=20, ge=1, title="Limit", description="Number of records to return"
    )


class FilterParams(FilterBase):
    result_type: Literal["publication", "software", "dataset", "other"] = "publication"


class FilterCountry(FilterParams):
    country: str | None = Field(default=None, examples=["KEN"], pattern="^([A-Z]{3})$")


class FilterOutputList(FilterCountry):
    pass


class FilterWorkstream(FilterBase):
    workstream: List[str] | None = Field(default=None)


class FilterAuthorDetail(FilterCountry):
    pass
