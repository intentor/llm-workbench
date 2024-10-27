"""Prompt structure module."""

from abc import abstractmethod
import re

from attr import dataclass

DEFAULT_PROMPT_PART_RETURN = ''


class Prompt():
    """Define a prompt structure."""

    PROMPT_PATTERN = r"(\:(?P<label>[a-z0-9-]+)\s)?(\/(?P<tool>[a-z]+)(\?(?P<params>[A-Za-z0-9&=\-_]+))?)?(\s?(?P<prompt>.*))?"
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

    def get_tool_name(self) -> str:
        """Return the tool name, if available."""
        label = self._match.group('tool')
        return label if label is not None else DEFAULT_PROMPT_PART_RETURN

    def get_tool_parameters(self) -> dict[str, str]:
        """Return the tool name, if available."""
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
    def generate(self, prompt: Prompt) -> GeneratedResponse:
        """Generates a respons based on a prompt.

        Args:
            - prompt: Prompt to generate a response.

        Returns:
            Response from the generation.
        """
        raise NotImplementedError()
