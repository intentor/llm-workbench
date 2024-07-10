"""Perform interactive operations with LLMs."""

from logging import getLogger

from ollama import Client

from core.indexer import ContextIndexer
from core.prompt import Prompt, PromptHistory, PromptHistoryEntry, PromptType, replace_response

logger = getLogger()


class PromptOperator():
    """Perform operations with prompts."""

    def __init__(
        self,
            history: PromptHistory,
            indexer: ContextIndexer,
            ollama: Client,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - history: Prompt history manager.
            - indexer: Index manager.
            - ollama: Client to access Ollama.
            - model_name: Name of the LLM model used for generation.
        """
        self._history = history
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

        Args:
            - prompt: Prompt to query the context.

        Returns:
            Response from the context or core.
        """

        prompt_processor = Prompt(prompt)
        prompt_text = replace_response(
            prompt_processor.get_prompt(), self._history)

        if prompt_processor.get_prompt_type() == PromptType.CONTEXT:
            response = self._indexer.query(
                prompt_text,
                prompt_processor.get_top_k())
        else:
            response = self._generate(prompt_text)

        prompt_label = prompt_processor.get_label()
        self._history.append(PromptHistoryEntry(
            label=prompt_label,
            prompt=prompt,
            response=response
        ))

        logger.debug('m=generate label= prompt=%s response=%s',
                     prompt_text, response)

        return response

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
