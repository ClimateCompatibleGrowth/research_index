from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List, Optional
from uuid import UUID

class Author(BaseModel):
    uuid: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    orcid: Optional[HttpUrl] = None

class DateTimeComponents(BaseModel):
    _Date__ordinal: Optional[int] = None
    _Date__year: Optional[int] = None
    _Date__month: Optional[int] = None
    _Date__day: Optional[int] = None

class TimeComponents(BaseModel):
    _Time__ticks: Optional[int] = None
    _Time__hour: Optional[int] = None
    _Time__minute: Optional[int] = None
    _Time__second: Optional[int] = None
    _Time__nanosecond: Optional[int] = None
    _Time__tzinfo: Optional[str] = None

class CitedByDateTime(BaseModel):
    _DateTime__date: Optional[DateTimeComponents] = None
    _DateTime__time: Optional[TimeComponents] = None

class OutputModel(BaseModel):
    uuid: UUID
    abstract: Optional[str] = None
    cited_by_count_date: Optional[CitedByDateTime] = None
    doi: Optional[str] = None
    publication_day: Optional[int] = None
    publication_month: Optional[int] = None
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    result_type: Optional[str] = None
    title: Optional[str] = None
    countries: List = Field(default_factory=list)
    authors: Optional[List[Author]] = Field(default_factory=list)