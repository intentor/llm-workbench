"""Selector based generation module."""

from logging import getLogger

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator

logger = getLogger()


class SelectorResponseGenerator(ResponseGenerator):
    """Generate responses from generators based on their types."""

    def __init__(
        self,
        generators: list[ResponseGenerator]
    ):
        """
        Args:
            - generators: Generators available for selection.
        """
        generators_per_type: dict[str, ResponseGenerator] = {}
        for generator in generators:
            generators_per_type[generator.get_type()] = generator

        self._generators = generators_per_type

    def get_type(self) -> str:
        return 'selector'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        generator_type = prompt.get_generator_type()

        if generator_type in self._generators:
            return self._generators[generator_type].generate(prompt)
        else:
            raise ValueError(
                f"Generator not available for type name {generator_type}.")
