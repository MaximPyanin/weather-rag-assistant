from weaviate import WeaviateClient, connect
from weaviate.classes.config import Property, DataType
from langchain.schema import Document
from langchain_weaviate import WeaviateVectorStore
from weaviate.collections import Collection
from weaviate.exceptions import UnexpectedStatusCodeError

from src.config.config_service import AppConfig
from src.adapters.vector_store_adapter import VectorStoreAdapter
from src.embeddings_providers.azure_embedding_service import AzureEmbeddingsService


class WeaviateVectorStoreAdapter(VectorStoreAdapter):
    def __init__(self, config: AppConfig, embedding: AzureEmbeddingsService):
        self.config = config
        self.client = WeaviateClient(
            connection_params=connect.ConnectionParams.from_params(
                http_host=self.config.HTTP_HOST,
                http_port=self.config.HTTP_PORT,
                http_secure=False,
                grpc_host=self.config.HTTP_HOST,
                grpc_port=self.config.GRPC_PORT,
                grpc_secure=False,
            )
        )
        self.client.connect()
        self.embedding = embedding

    def add_documents(
        self, documents: list[Document], collection: str, **kwargs
    ) -> None:
        coll = self._ensure(collection)
        texts = [d.page_content for d in documents]
        vectors = self.embedding.embed_documents(texts)

        with coll.batch.dynamic() as batch:
            for doc, vec in zip(documents, vectors):
                batch.add_object(
                    properties={"content": doc.page_content, **doc.metadata},
                    vector=vec,
                )

    def get_retriever(self, collection: str, k: int = 1):
        store = WeaviateVectorStore(
            client=self.client,
            index_name=collection,
            text_key="content",
            embedding=self.embedding,
        )
        return store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )

    def clear_collection(self, collection: str) -> None:
        if self.collection_exists(collection):
            return self.client.collections.delete(collection)
        return None

    def collection_exists(self, collection: str) -> bool:
        meta = self.client.collections.list_all()

        return any(item == collection for item in meta)

    def _ensure(self, collection: str) -> Collection:
        if not self.collection_exists(collection):
            try:
                self.client.collections.create(
                    name=collection,
                    vectorizer_config=None,
                    properties=[
                        Property(name="content", data_type=DataType.TEXT),
                        Property(name="city", data_type=DataType.TEXT),
                    ],
                )
            except UnexpectedStatusCodeError as e:
                if "already exists" not in str(e):
                    raise
        return self.client.collections.get(collection)

    def close(self) -> None:
        return self.client.close()
