"""Model executor module."""

from logging import getLogger

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator
from core.prompting.history import (
    PromptHistory,
    PromptHistoryEntry,
    PromptHistoryReplacer
)

logger = getLogger()


class PromptExecutor():
    """Executes a prompt considering any avaliable generators."""

    def __init__(
        self,
        history: PromptHistory,
        generators: list[ResponseGenerator]
    ):
        """
        Args:
            - history: Prompt history manager.
            - generators: Generators available for prompt execution.
        """
        self._history = history
        self._replacer = PromptHistoryReplacer(history)

        generators_per_type: dict[str, ResponseGenerator] = {}
        for generator in generators:
            generators_per_type[generator.get_type()] = generator

        self._generators = generators_per_type

    def execute(self, prompt: str) -> GeneratedResponse:
        """Executes a prompt.

        Args:
            - Prompt to be executed.

        Returns:
            Generated response from the prompt execution.
        """
        replaced_prompt = self._replacer.replace(prompt)
        prompt_structure = Prompt(replaced_prompt)
        generator_type = prompt_structure.get_generator_type()

        if generator_type in self._generators:
            generated_response = self._generators[generator_type].generate(
                prompt_structure)

            self._append_history(prompt_structure, generated_response)

            logger.debug(
                'm=generate type=%s params=%s prompt=%s response=%s',
                generator_type,
                prompt_structure.get_generator_parameters(),
                prompt,
                generated_response)

            return generated_response
        else:
            raise ValueError(
                f"Generator not available for type name {generator_type}.")

    def _append_history(self, prompt: Prompt, response: GeneratedResponse):
        self._history.append(PromptHistoryEntry(
            label=prompt.get_label(),
            prompt=prompt.get_original_prompt(),
            response=response
        ))
