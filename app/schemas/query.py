from typing import Literal

from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException


class FilterBase(BaseModel):
    skip: int = Field(default=0, ge=0, title="Skip", description="Number of records to skip")
    limit: int = Field(default=20, ge=1, title="Limit", description="Number of records to return")


class FilterParams(FilterBase):
    result_type: Literal["publication", "software", "dataset", "other"] = "publication"


class FilterCountry(FilterParams):
    country: str | None = Field(default=None, examples=['KEN'], pattern="^([A-Z]{3})$")


class FilterOutputList(FilterCountry):
    pass

class FilterWorkstream(BaseModel):
    workstream: str | None = Field(default=None)


class FilterAuthorDetail(FilterCountry):
    pass