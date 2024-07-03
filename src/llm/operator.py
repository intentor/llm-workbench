"""Perform interactive operations with an LLM."""

import re
from typing import List
from logging import getLogger

from ollama import Client

from llm.indexer import ContextIndexer

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

        prompt_processor = PromptProcessor(prompt)
        actual_prompt = prompt_processor.get_prompt()
        if prompt_processor.is_context_prompt():
            return self._indexer.query(
                actual_prompt,
                prompt_processor.get_top_k())
        else:
            return self._generate(actual_prompt)

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


class PromptProcessor():
    """Define a prompt to be sent to a LLM."""

    CONTEXT_PATTERN = r"(?P<get_context>/context(\:(?P<context_size>\d+))?\s)?(?P<prompt>.*)"
    """Regex pattern for the prompt structure."""

    def __init__(self, text: str):
        """
        Args:
            - text: Prompt text.
        """
        regex = re.compile(self.CONTEXT_PATTERN, re.DOTALL)
        self._match = regex.match(text)

    def is_context_prompt(self) -> bool:
        """Return whether this is a prompt to query context."""
        return True if self._match.group(
            'get_context') is not None else False

    def get_top_k(self, default_top_k: int = DEFAULT_SIMILARITY_TOP_K) -> int:
        """Return the Similarity Top-K value in the prompt."""
        context_size = self._match.group('context_size')
        top_k = default_top_k if context_size is None else int(context_size)
        return top_k

    def get_prompt(self) -> str:
        """Return the actual prompt text."""
        return self._match.group('prompt')
