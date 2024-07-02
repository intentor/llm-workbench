"""Perform interactive operations with an LLM."""

import re
from typing import List
from logging import getLogger

from ollama import Client

from llm.indexer import ContextIndexer

CONTEXT_PATTERN = r"(?P<get_context>/context(\:(?P<context_size>\d+))?\s)?(?P<prompt>.*)"
DEFAULT_SIMILARITY_TOP_K = 4

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
        self._context_regex = re.compile(CONTEXT_PATTERN, re.DOTALL)

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

        match = self._context_regex.match(prompt)
        query_context = True if match.group(
            'get_context') is not None else False

        if query_context:
            actual_prompt = match.group('prompt')
            context_size = match.group('context_size')
            similarity_top_k = DEFAULT_SIMILARITY_TOP_K if context_size is None else int(
                context_size)
            return self._indexer.query(actual_prompt, similarity_top_k)
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
