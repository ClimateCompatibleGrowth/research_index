from typing import Tuple

from fastapi import APIRouter, HTTPException, UploadFile

from app.crud.ingest import Ingest
from app.schemas.ingest import IngestionMetrics, IngestionStates

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/ingest_dois")
async def ingest_dois(
    file: UploadFile, limit: int=50, update_metadata: bool=False
) -> Tuple[IngestionMetrics, IngestionStates]:
    try:
        content = await file.read()
        dois = [line.strip() for line in content.decode().split("\n") if line.strip()]
        if not dois:
            raise HTTPException(status_code=400, detail="No valid DOIs found in file")
        ingest = Ingest(dois=dois, limit=limit, update_metadata=update_metadata)
        return ingest.ingest_dois()
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
