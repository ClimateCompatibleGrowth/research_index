from typing import Dict, List, Optional

from pydantic import BaseModel, Field

class Count(BaseModel):
    """Represents count of the outputs
    ```json
        {'total': 245684392,
        'publication': 1234,
        'software': 5678,
        'dataset': 1234,
        'other': 39494},
     ```
    """

    total: int
    publication: int
    software: int
    dataset: int
    other: int


class Meta(BaseModel):
    """
    Base data model representing an academic author or contributor
    with their associated metadata.

    ```json
    "count": {}
    "db_response_time_ms": 929,
    "page": 1,
    "per_page": 25
    ```

    """
    count: Count | None
    db_response_time_ms: int
    page: int
    per_page: int
