from typing import Any


from langchain.schema import Document


from src.config.config_service import AppConfig

from src.adapters.weaviate_adapter import WeaviateVectorStoreAdapter


class IndexerService:
    def __init__(self, config: AppConfig, store: WeaviateVectorStoreAdapter):
        self.config = config
        self.store = store
        self.collection = self.config.COLLECTION_NAME

    def index_weather(self, records: list[dict[str, Any]]) -> None:
        if self.store.collection_exists(self.collection):
            self.store.clear_collection(self.collection)

        docs = [
            Document(
                page_content=(
                    f"City: {r['city']}. "
                    f"Temperature: {r['temperature_c']} °C. "
                    f"Wind speed: {r['wind_speed_kmh']} km/h."
                ),
                metadata={"city": r["city"]},
            )
            for r in records
        ]
        return self.store.add_documents(docs, self.collection)
