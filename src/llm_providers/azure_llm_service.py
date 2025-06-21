from langchain_openai import AzureChatOpenAI  # ← новый импорт
from src.config.config_service import AppConfig
from src.llm_providers.base_llm_service import BaseLLMService


class AzureLLMService(BaseLLMService):
    def __init__(self, config: AppConfig):
        self.__llm = AzureChatOpenAI(
            azure_deployment=config.AZURE_OPENAI_LLM_DEPLOYMENT,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            openai_api_version=config.AZURE_OPENAI_API_VERSION,
            api_key=config.AZURE_OPENAI_KEY,
            temperature=config.TEMPERATURE,
            top_p=config.TOP_P,
            max_tokens=config.MAX_NEW_TOKENS,
        )

    @property
    def get_llm(self) -> AzureChatOpenAI:
        return self.__llm
