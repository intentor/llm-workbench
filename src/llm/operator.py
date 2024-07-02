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
            ollama: Client,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - indexer: Index manager.
            - ollama: Client to access Ollama.
            - model_name: Name of the LLM model used for generation.
        """
        self._indexer = indexer
        self._ollama = ollama
        self._model_name = model_name

    def index_files(
        self,
        files_path: List[str],
        chunk_size: int,
        chunk_overlap: int
    ):
        """Index files in the context.

        Args:
            - files_path: Path of each file to be indexed.
            - chunk_size: Size when splitting documents. The smaller,
                the more precise.
            - chunk_overlap: Amount of overlap when splitting documents into chunk_size.
        """
        self._indexer.index_files(files_path, chunk_size, chunk_overlap)

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
        response = self._ollama.generate(self._model_name, prompt)
        logger.info('m=generate response=%s', response)

        return response['response']
