"""
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from src.embeddings_providers.base_embedding_service import BaseEmbeddingService
from src.config.config_service import AppConfig


class TransformerEmbeddings(BaseEmbeddingService,Embeddings):
    def __init__(self, config: AppConfig):
        self.config = config
        self.__embedder = SentenceTransformer(self.config.EMBEDDING_MODEL_ID)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.__embedder.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    @property
    def embeddings(self) -> SentenceTransformer:
        return self.__embedder
"""
