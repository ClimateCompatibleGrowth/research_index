from typing import List

from pydantic import BaseModel


class IngestionMetrics(BaseModel):
    submitted_dois: int
    processed_dois: int
    new_dois: int
    existing_dois: int
    updated_existing_dois: int
    ingested_dois: int
    metadata_pass: int
    metadata_failure: int
    valid_pattern_dois: int
    invalid_pattern_dois: int
    openalex_success: int
    openaire_success: int
    total_time_seconds: float


class IngestionStates(BaseModel):
    submitted_dois: List[str]
    processed_dois: List[str]
    new_dois: List[str]
    existing_dois: List[str]
    updated_existing_dois: List[str]
    ingested_dois: List[str]
    metadata_pass: List[str]
    metadata_failure: List[str]
    openalex_success: List[str]
    openaire_success: List[str]
    valid_pattern_dois: List[str]
    invalid_pattern_dois: List[str]
