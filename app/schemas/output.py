from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from uuid import UUID
from .author import AuthorBase
from . import CountryBaseModel
from .meta import MetaPublication
from .topic import TopicBaseModel


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
    """Schema for an Output

    An output should look like this:

    ```json
        {
        "uuid": "f05b1fc5-f831-4755-966f-06de074ab51c", # required
        "doi": "http://doi.org/10.5281/zenodo.7015450", # required
        "title": 'An example title', # required
        "abstract": 'A long abstract', # optional
        "journal": "Applied JSON", # optional
        "cited_by_count_date": '2024-03-01', # optional
        "cited_by_count": 34, # optional
        "openalex": "https://openalex.org/W4393416420", # optional
        "publication_day": 03, # optional
        "publication_month": 12, # optional
        "publication_year": 2023, # optional
        "publisher": "Elsevier", # optional
        "result_type": 'publication', # required
        "countries": ['KEN', 'BEN'], # optional
        "author": [
                    {
                    "uuid": "c613b25b-967c-4586-9101-ece3a901fd9c",
                    "first_name": "Will",
                    "last_name": "Usher",
                    "orcid": "https://orcid.org/0000-0001-9367-1791",
                    }
                    ] # required
        }
    ```
    """
    uuid: UUID
    doi: str = Field(pattern=r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$")
    title: str
    result_type: str
    authors: List[AuthorBase]
    abstract: Optional[str] = None
    journal: Optional[str] = None  # Only academic publications have a journal
    cited_by_count_date: Optional[CitedByDateTime] = None
    cited_by_count: Optional[int] = None
    publication_day: Optional[int] = None
    publication_month: Optional[int] = None
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    countries: Optional[List[CountryBaseModel]] = Field(default_factory=list)
    topics: Optional[List[TopicBaseModel]] = Field(default_factory=list)


class OutputListModel(BaseModel):
    """Represents a list of outputs including metadata

    """
    meta: MetaPublication
    results: List[OutputModel]
