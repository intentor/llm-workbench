"""Model generation module."""

from core.prompting.base import (
    DEFULT_GENERATOR_TYPE,
    GeneratedResponse,
    ModelProvider,
    Prompt
)
from core.prompting.history import HistoryAwareResponseGeneator, PromptHistory


class ModelResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from an LLM using Ollama."""

    def __init__(
        self,
            history: PromptHistory,
            provider: ModelProvider
    ):
        """
        Args:
            - history: Prompt history manager.
            - provider: Provider for generating responses from a model.
        """
        super().__init__(history)
        self._provider = provider

    def get_type(self) -> str:
        return DEFULT_GENERATOR_TYPE

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())
        generated_response = self._provider.generate(prompt_text)
        self._append_history(prompt, generated_response)

        return generated_response
