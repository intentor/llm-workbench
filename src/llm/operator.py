"""Perform interactive operations with an LLM."""

import time
from typing import List
from logging import getLogger

from ollama import Client

CONTEXT_KEY = '/context'

logger = getLogger()


class LlmOperator():
    """Operates an LLM."""

    def __init__(
        self,
            ollama_host: str = 'http://localhost:11434',
            model_name: str = 'llama3',
            request_timeout: int = 300.0
    ):
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

        logger.info('m=index files=%s', files_path)
        time.sleep(2)
        return

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

        time.sleep(2)
        if prompt.startswith(CONTEXT_KEY):
            actual_prompt = prompt[len(CONTEXT_KEY):]
            return self._query(actual_prompt)
        else:
            return self._generate(prompt)

    def _query(self, prompt: str) -> str:
        """Query the context.

        Args:
            - prompt: Prompt to query the context.

        Returns:
            Context found or empty string.
        """

        logger.info('m=query prompt=%s', prompt)
        return f"Context.\n{prompt}"

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
