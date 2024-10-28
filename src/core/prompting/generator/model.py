"""Model generation module."""

from core.prompting.base import (
    DEFULT_GENERATOR_TYPE,
    GeneratedResponse,
    ModelProvider,
    Prompt,
    ResponseGenerator
)


class ModelResponseGenerator(ResponseGenerator):
    """Generate responses from an LLM using Ollama."""

    def __init__(
        self,
            provider: ModelProvider
    ):
        """
        Args:
            - provider: Provider for generating responses from a model.
        """
        self._provider = provider

    def get_type(self) -> str:
        return DEFULT_GENERATOR_TYPE

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        return self._provider.generate(prompt.get_prompt())
