"""Prompt management module."""

import re
from enum import Enum
from logging import getLogger

from attr import dataclass

DEFAULT_SIMILARITY_TOP_K = 4
HISTORY_ITEM_SEPARATOR = '\n\n'

logger = getLogger()


class PromptType(Enum):
    """Prompt type."""
    GENERATE = 1
    CONTEXT = 2
    ENDPOINT = 3
    ECHO = 4
    TEMPLATE = 5


class Prompt():
    """Define a prompt that will perform an action."""

    PROMPT_PATTERN = r"(\:(?P<label>[a-z0-9-]+)\s)?(?P<context>\/context(\:(?P<context_size>\d+))?(\?file=\"(?P<filename>[\w\.\- ]+)\")?\s)?(?P<endpoint>\/get\:)?(?P<echo>\/echo\s)?(?P<template>\/template\s)?(?P<prompt>.*)"
    """Regex pattern for the prompt structure."""

    def __init__(self, text: str):
        """
        Args:
            - text: Prompt text.
        """
        pattern = re.compile(self.PROMPT_PATTERN, re.DOTALL)
        self._match = pattern.match(text)

        self._original_prompt = text

        if self._match.group('context') is not None:
            self._type = PromptType.CONTEXT
        elif self._match.group('endpoint') is not None:
            self._type = PromptType.ENDPOINT
        elif self._match.group('echo') is not None:
            self._type = PromptType.ECHO
        elif self._match.group('template') is not None:
            self._type = PromptType.TEMPLATE
        else:
            self._type = PromptType.GENERATE

    def get_original_prompt(self) -> str:
        """Return the original prompt value."""
        return self._original_prompt

    def get_prompt_type(self) -> PromptType:
        """Return the type of the prompt."""
        return self._type

    def get_label(self) -> str:
        """Return the prompt label."""
        label = self._match.group('label')
        return label if label is not None else ''

    def get_top_k(self, default_top_k: int = DEFAULT_SIMILARITY_TOP_K) -> int:
        """Return the Similarity Top-K value in the prompt."""
        context_size = self._match.group('context_size')
        top_k = default_top_k if context_size is None else int(context_size)
        return top_k

    def get_file_name(self):
        """Return the context file name filter."""
        label = self._match.group('filename')
        return label if label is not None else ''

    def get_prompt(self) -> str:
        """Return the actual prompt text."""
        return self._match.group('prompt')


@dataclass
class GeneratedResponse():
    """Defines a generated response."""

    value: str
    """Response generated."""

    input_tokens: int = 0
    """Total number of input tokens. Can be 0 in case no model was used."""

    output_tokens: int = 0
    """Total number of output tokens. Can be 0 in case no model was used."""


@dataclass
class PromptHistoryEntry():
    """Defines an entry in the prompt history."""

    label: str
    """Label of the prompt item."""

    prompt: str
    """Prompt that performed an action."""

    response: GeneratedResponse
    """Response from the prompt action."""


class PromptHistory(list[PromptHistoryEntry]):
    """Manages prompt history."""

    def get_prompts(self) -> list[str]:
        """Get all prompts in the history."""
        return [entry.prompt for entry in self]

    def get_last_response(self) -> str:
        """Get the last response in the history."""
        return self[-1].response.value if self else ''

    def get_response_by_label(self, label: str) -> list[str]:
        """Get response by label.

        Args:
            - label: Label to look for.
        """
        return [entry.response.value for entry in self if entry.label == label]

    def get_as_string(self) -> str:
        """Get the entire history as string, with messages separated by
        line breaks."""
        return HISTORY_ITEM_SEPARATOR.join(
            [item.prompt + HISTORY_ITEM_SEPARATOR +
                item.response.value for item in self]
        )

    def get_total_input_tokens(self) -> int:
        """Get the total number of input tokens of entries in the history."""
        return sum(entry.response.input_tokens for entry in self)

    def get_total_output_tokens(self) -> int:
        """Get the total number of output tokens of entries in the history."""
        return sum(entry.response.output_tokens for entry in self)


class PromptPatternReplacer():
    """Replaces text on prompts based on certain patterns."""

    REPLACEMENT_PATTERN = r"(\{response\:(?P<type>last|label)(\:(?P<label>[a-z0-9-]+))?\})"
    """Regex pattern for prompt replacement."""

    def __init__(self, history: PromptHistory):
        self._history = history

    def replace(self, prompt: str) -> str:
        """Replace responses in a prompt, either with label or not.
        If no replacement key is found, no replacement is made.

        Args:
            - prompt: Prompt in which replacements will take place.
            - history: Prompt history to look for previous responses.

        Returns:
            Prompt with previous response replaced.
        """

        return re.sub(
            self.REPLACEMENT_PATTERN,
            self._evaluate_replacement,
            prompt
        )

    def _evaluate_replacement(self, match):
        if match.group('type') == 'last':
            return self._history.get_last_response()
        elif match.group('type') == 'label':
            entries: list[str] = self._history.get_response_by_label(
                match.group('label'))
            return '\n'.join(entries)
        else:
            return ''
