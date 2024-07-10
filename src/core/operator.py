"""Perform interactive operations with LLMs."""

from logging import getLogger

from ollama import Client

from core.indexer import ContextIndexer
from core.prompt import Prompt

logger = getLogger()


class LlmOperator():
    """Operates an core."""

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
        files_path: list[str],
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
        Case else, the prompt is sent to the core.

        Args:
            - prompt: Prompt to query the context.

        Returns:
            Response from the context or core.
        """

        prompt_processor = Prompt(prompt)
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
            - prompt: Prompt to be sent to the core.

        Returns:
            Response from the core.
        """
        logger.info('m=generate prompt=%s', prompt)
        response = self._ollama.generate(self._model_name, prompt)
        logger.info('m=generate response=%s', response)

        return response['response']
