from typing import List
from fastapi import APIRouter
from app.schemas.topic import TopicBaseModel


router = APIRouter(
    prefix="/api/topics",
    tags=["countries"]
)

@router.get("")
def api_topics_list() -> List[TopicBaseModel]:
    raise NotImplementedError("Have not yet implemented topics in the database")


@router.get("/{id}")
def api_topics_list(id: str) -> TopicBaseModel:
    raise NotImplementedError("Have not yet implemented topics in the database")