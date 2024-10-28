"""Ollama generation module."""

from ollama import Client

from core.prompting.base import (
    GeneratedResponse,
    ModelProvider
)


class OllamaModelProvider(ModelProvider):
    """Generate responses from an LLM using Ollama."""

    def __init__(
        self,
            ollama: Client,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - ollama: Client to access Ollama.
            - model_name: Name of the LLM model used for generation.
        """
        self._ollama = ollama
        self._model_name = model_name

    def generate(self, prompt: str) -> GeneratedResponse:
        ollama_response = self._ollama.generate(self._model_name, prompt)

        generated_response = GeneratedResponse(
            value=ollama_response['response'],
            input_tokens=ollama_response['prompt_eval_count'],
            output_tokens=ollama_response['eval_count']
        )

        return generated_response
