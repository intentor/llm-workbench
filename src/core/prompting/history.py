"""Prompt history module."""

import re

from attr import dataclass

from core.prompting.base import GeneratedResponse

HISTORY_ITEM_SEPARATOR = '\n\n'


@dataclass
class PromptHistoryEntry():
    """Defines an entry in the prompt history."""

    label: str
    """Prompt label."""

    prompt: str
    """Original prompt."""

    response: GeneratedResponse
    """Response generated from the prompt."""


class PromptHistory(list[PromptHistoryEntry]):
    """Manages prompt history."""

    def __str__(self):
        """Get the entire history as string, with messages separated by
        line breaks."""
        return HISTORY_ITEM_SEPARATOR.join(
            [item.prompt + HISTORY_ITEM_SEPARATOR +
                item.response.value for item in self]
        )

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

    def get_total_input_tokens(self) -> int:
        """Get the total number of input tokens of entries in the history."""
        return sum(entry.response.input_tokens for entry in self)

    def get_total_output_tokens(self) -> int:
        """Get the total number of output tokens of entries in the history."""
        return sum(entry.response.output_tokens for entry in self)


class PromptHistoryReplacer():
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
