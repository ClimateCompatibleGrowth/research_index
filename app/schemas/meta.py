from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class CountPublication(BaseModel):
    """Represents count of the outputs
    ```json
        {'total': 245684392,
         'publication': 1234,
         'software': 5678,
         'dataset': 1234,
         'other': 39494},
     ```
    """

    total: int = 0
    publication: int = 0
    software: int = 0
    dataset: int = 0
    other: int = 0


class CountAuthor(BaseModel):
    """Represents a count of the authors or countries"""
    total: int = 0


class Pagination(BaseModel):
    """Used for lists"""

    count: CountAuthor
    skip: int
    limit: int


class MetaPublication(BaseModel):
    """
    Base data model representing an academic author or contributor
    with their associated metadata.

    ```json
    "count": {'total': 245684392,
              'publication': 1234,
              'software': 5678,
              'dataset': 1234,
              'other': 39494}
    ```

    """
    count: CountPublication | None
    skip: int
    limit: int
    result_type: str | None


class MetaAuthor(BaseModel):
    """
    Base data model representing an academic author or contributor
    with their associated metadata.

    ```json
    "count": {'total': 42}
    ```

    """
    count: CountAuthor | None
    skip: int
    limit: int
