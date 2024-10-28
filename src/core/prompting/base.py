"""Prompt structure module."""

from abc import abstractmethod
from logging import getLogger
import re

from attr import dataclass

logger = getLogger()

DEFAULT_PROMPT_PART_RETURN = ''
DEFULT_GENERATOR_TYPE = 'model'


class Prompt():
    """Define a prompt structure."""

    PROMPT_PATTERN = r"(\:(?P<label>[a-z0-9-]+)\s)?(\/(?P<generator>[a-z]+)(\?(?P<params>[A-Za-z0-9&=\.\-_]+))?)?(\s?(?P<prompt>.*))?"
    """Regex pattern for the prompt structure."""

    def __init__(self, text: str):
        """
        Args:
            - text: Prompt text.
        """
        self._original_prompt = text
        pattern = re.compile(self.PROMPT_PATTERN, re.DOTALL)
        self._match = pattern.match(text)

    def __str__(self):
        return self._original_prompt

    def get_original_prompt(self) -> str:
        """Return the original prompt value."""
        return self._original_prompt

    def get_prompt(self) -> str:
        """Return the prompt text."""
        prompt = self._match.group('prompt')
        return prompt.strip() if prompt is not None else DEFAULT_PROMPT_PART_RETURN

    def get_label(self) -> str:
        """Return the prompt label."""
        label = self._match.group('label')
        return label if label is not None else DEFAULT_PROMPT_PART_RETURN

    def get_generator_type(self) -> str:
        """Return the name/type of the generator to be used for this prompt."""
        label = self._match.group('generator')
        return label if label is not None else DEFULT_GENERATOR_TYPE

    def get_generator_parameters(self) -> dict[str, str]:
        """Return the generator parameters, if available."""
        parameters_text = self._match.group('params')

        parameters = {}

        if parameters_text is not None:
            parameters_pairs = parameters_text.split('&')
            for parameter_pair in parameters_pairs:
                key, value = parameter_pair.split('=')
                parameters[key] = value

        return parameters


@dataclass
class GeneratedResponse():
    """Defines a generated response."""

    value: str
    """Response generated."""

    input_tokens: int = 0
    """Total number of input tokens. Can be 0 in case no model was used."""

    output_tokens: int = 0
    """Total number of output tokens. Can be 0 in case no model was used."""


class ResponseGenerator():
    """Generate responses based on a prompt."""

    @abstractmethod
    def get_type(self) -> str:
        """Get the type name of the generator."""
        raise NotImplementedError()

    @abstractmethod
    def generate(self, prompt: Prompt) -> GeneratedResponse:
        """Generates a response based on a prompt.

        Args:
            - prompt: Prompt to generate a response.

        Returns:
            Response from the generation.
        """
        raise NotImplementedError()


class ModelProvider():
    """Provides model prompt execution for response generation."""

    @abstractmethod
    def generate(self, prompt: str) -> GeneratedResponse:
        """Generates a response based on a prompt.

        Args:
            - prompt: Prompt to generate a response.

        Returns:
            Response from the generation.
        """
        raise NotImplementedError()


class PromptExecutor():
    """Executes a prompt considering any avaliable generators."""

    def __init__(
        self,
        generators: list[ResponseGenerator]
    ):
        """
        Args:
            - generators: Generators available for prompt execution.
        """
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
        prompt_structure = Prompt(prompt)
        generator_type = prompt_structure.get_generator_type()

        if generator_type in self._generators:
            generated_response = self._generators[generator_type].generate(
                prompt_structure)

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


class GenerationError(Exception):
    def __init__(self, message: str = 'Error when performing generation.'):
        super().__init__(message)
