from typing import Tuple

from app.schemas.ingest import IngestionMetrics, IngestionStates
from research_index_backend.create_graph_from_doi import add_country_relations, main


class Ingest:
    def __init__(
        self, dois: list, limit: int, update_metadata: bool
    ) -> Tuple[IngestionMetrics, IngestionStates]:
        self.dois = dois
        self.limit = limit
        self.update_metadata = update_metadata

    def ingest_dois(self):
        try:
            doi_manager = main(
                self.dois, limit=self.limit, update_metadata=self.update_metadata
            )
        except Exception as e:
            print(f"Error ingesting dois: {e}")
        try:
            add_country_relations()
        except Exception as e:
            print(f"Error addding country relations: {e}")

        return doi_manager.ingestion_metrics()
