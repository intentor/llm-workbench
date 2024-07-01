"""Perform interactive operations with an LLM."""

from typing import List
from logging import getLogger

from ollama import Client

from llm.indexer import ContextIndexer

CONTEXT_KEY = '/context'

logger = getLogger()


class LlmOperator():
    """Operates an LLM."""

    def __init__(
        self,
            indexer: ContextIndexer,
            ollama_host: str = 'http://localhost:11434',
            model_name: str = 'llama3',
            request_timeout: int = 300.0
    ):
        """
        Args:
            - indexer: Index manager.
            - ollama_host: ost of the Ollama server.
            - model_name: Name of the LLM model used for generation.
            - request_timeout: Request timeout to the Ollama server.
        """
        self._indexer = indexer
        self._llm_client = Client(
            host=ollama_host,
            timeout=request_timeout
        )
        self._model_name = model_name
        self._request_timeout = request_timeout

    def index_files(self, files_path: List[str]):
        """Index files in the context.

        Args:
            - files_path: Path of each file to be indexed.
        """
        self._indexer.index_files(files_path)

    def generate(self, prompt: str) -> str:
        """Generates a response.
        If prompt starts with /context, everything after this key will be used
        as prompt to query the context.
        Case else, the prompt is sent to the LLM.

        Args:
            - prompt: Prompt to query the context.

        Returns:
            Response from the context or LLM.
        """
        if prompt.startswith(CONTEXT_KEY):
            actual_prompt = prompt[len(CONTEXT_KEY):]
            return self._indexer.query(actual_prompt)
        else:
            return self._generate(prompt)

    def _generate(self, prompt: str) -> str:
        """Generate a response from a prompt.

        Args:
            - prompt: Prompt to be sent to the LLM.

        Returns:
            Response from the LLM.
        """
        logger.info('m=generate prompt=%s', prompt)
        response = self._llm_client.generate(self._model_name, prompt)
        logger.info('m=generate response=%s', response)

        return response['response']
