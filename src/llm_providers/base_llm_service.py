from abc import ABC, abstractmethod
from typing import Any


class BaseLLMService(ABC):
    @property
    @abstractmethod
    def get_llm(self) -> Any: ...
