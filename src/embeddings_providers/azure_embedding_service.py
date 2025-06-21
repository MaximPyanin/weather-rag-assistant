from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings

from src.config.config_service import AppConfig
from langchain.embeddings.base import Embeddings


class AzureEmbeddingsService(Embeddings):
    def __init__(self, config: AppConfig):
        self.__embeddings = AzureOpenAIEmbeddings(
            model=config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            azure_endpoint=config.AZURE_OPENAI_EMBEDDING_ENDPOINT,
            api_key=config.AZURE_OPENAI_KEY,
            api_version=config.AZURE_OPENAI_API_VERSION,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.__embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.__embeddings.embed_query(text)

    @property
    def embeddings(self) -> AzureOpenAIEmbeddings:
        return self.__embeddings
