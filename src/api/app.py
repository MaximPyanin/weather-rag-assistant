from flask import Flask
from flask_restx import Api
from src.config.config_service import AppConfig
from src.embeddings_providers.azure_embedding_service import AzureEmbeddingsService
from src.llm_providers.azure_llm_service import AzureLLMService
from src.services.crawling_service import CrawlingService
from src.adapters.weaviate_adapter import WeaviateVectorStoreAdapter
from src.services.indexer_service import IndexerService
from src.services.qa_service import QAService
from src.controllers.weather_controller import WeatherController
from .models.weather_models import WeatherModels
from .routes.weather_routes import WeatherRoutes
import os


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(
        app,
        version="1.0",
        title="Weather RAG API",
        description="Retrieval-augmented Weather Assistant",
        doc="/swagger/",
    )

    config = AppConfig(os.environ)
    embeddings = AzureEmbeddingsService(config)
    store_adapter = WeaviateVectorStoreAdapter(config, embeddings)
    crawling_service = CrawlingService(config)
    indexer_service = IndexerService(config, store_adapter)
    llm_service = AzureLLMService(config)
    qa_service = QAService(indexer_service, llm_service, config)
    controller = WeatherController(qa_service, indexer_service, crawling_service)

    @app.teardown_appcontext
    def shutdown_services(exception=None):
        try:
            crawling_service.close()
        finally:
            controller.clear_weather_index()

    controller.ensure_index()

    WeatherModels.init_models(api)
    WeatherRoutes.init_routes(api, controller)

    return app
