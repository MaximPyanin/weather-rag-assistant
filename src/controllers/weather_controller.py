from src.services.qa_service import QAService
from src.services.indexer_service import IndexerService
from src.services.crawling_service import CrawlingService


class WeatherController:
    def __init__(
        self,
        qa_service: QAService,
        indexer_service: IndexerService,
        crawling_service: CrawlingService,
    ):
        self.qa_service = qa_service
        self.indexer_service = indexer_service
        self.crawling_service = crawling_service

    def ask_weather(self, query: str) -> str:
        return self.qa_service.ask(query)

    def refresh_weather_data(self) -> None:
        weather_records = self.crawling_service.get_all_cities()
        return self.index_weather_data(weather_records)

    def index_weather_data(self, records: list[dict]) -> None:
        return self.indexer_service.index_weather(records)

    def clear_weather_index(self) -> None:
        if self.indexer_service.store.collection_exists(
            self.indexer_service.collection
        ):
            return self.indexer_service.store.clear_collection(
                self.indexer_service.collection
            )
        return None

    def index_status(self) -> bool:
        return self.indexer_service.store.collection_exists(
            self.indexer_service.collection
        )

    def ensure_index(self) -> None:
        if not self.index_status():
            self.refresh_weather_data()
