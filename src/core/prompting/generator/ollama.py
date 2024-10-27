"""Ollama generation module."""

from logging import getLogger

from ollama import Client

from core.prompting.base import (
    DEFULT_GENERATOR_TYPE,
    GeneratedResponse,
    Prompt
)
from core.prompting.history import HistoryAwareResponseGeneator, PromptHistory

logger = getLogger()


class OllamaResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from an LLM using Ollama."""

    def __init__(
        self,
            history: PromptHistory,
            ollama: Client,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - history: Prompt history manager.
            - ollama: Client to access Ollama.
            - model_name: Name of the LLM model used for generation.
        """
        super().__init__(history)
        self._ollama = ollama
        self._model_name = model_name

    def get_type(self) -> str:
        return DEFULT_GENERATOR_TYPE

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())
        ollama_response = self._ollama.generate(self._model_name, prompt_text)
        response = ollama_response['response']

        generated_response = GeneratedResponse(
            value=response,
            input_tokens=ollama_response['prompt_eval_count'],
            output_tokens=ollama_response['eval_count']
        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=ollama prompt=%s response=%s',
                     prompt_text, generated_response)

        return generated_response
