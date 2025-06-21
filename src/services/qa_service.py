from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from src.config.config_service import AppConfig
from src.llm_providers.azure_llm_service import AzureLLMService
from src.prompts.system_prompt import SYSTEM_PROMPT

from src.services.indexer_service import IndexerService


class QAService:
    def __init__(
        self, indexer: IndexerService, llm_service: AzureLLMService, config: AppConfig
    ):
        retriever = indexer.store.get_retriever(config.COLLECTION_NAME)

        combine_docs_chain = create_stuff_documents_chain(
            llm_service.get_llm, SYSTEM_PROMPT
        )
        self.chain = create_retrieval_chain(retriever, combine_docs_chain)
        self.retriever = retriever

    def ask(self, question: str) -> str:
        return self.chain.invoke({"input": question})["answer"]
