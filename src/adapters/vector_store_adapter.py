from abc import ABC, abstractmethod
from typing import List, Any


class VectorStoreAdapter(ABC):
    @abstractmethod
    def add_documents(
        self, documents: List[Any], collection: str, **kwargs
    ) -> None: ...

    @abstractmethod
    def get_retriever(self, collection: str): ...

    @abstractmethod
    def clear_collection(self, collection: str) -> None: ...

    @abstractmethod
    def collection_exists(self, collection: str) -> bool: ...
