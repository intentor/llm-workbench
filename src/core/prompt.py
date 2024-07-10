"""Prompt management module."""

import re
from logging import getLogger

DEFAULT_SIMILARITY_TOP_K = 4

logger = getLogger()


class Prompt():
    """Define a prompt to be sent to a core."""

    CONTEXT_PATTERN = r"(\:(?P<label>[a-z0-9-]+)\s)?(?P<get_context>/context(\:(?P<context_size>\d+))?\s)?(?P<prompt>.*)"
    """Regex pattern for the prompt structure."""

    def __init__(self, text: str):
        """
        Args:
            - text: Prompt text.
        """
        regex = re.compile(self.CONTEXT_PATTERN, re.DOTALL)
        self._original_prompt = text
        self._match = regex.match(text)

    def is_context_prompt(self) -> bool:
        """Return whether this is a prompt to query context."""
        return True if self._match.group(
            'get_context') is not None else False

    def get_original_prompt(self) -> str:
        """Return the original prompt value."""
        return self._original_prompt

    def get_label(self) -> str:
        """Return the label in the context."""
        label = self._match.group('label')
        return label if label is not None else ''

    def get_top_k(self, default_top_k: int = DEFAULT_SIMILARITY_TOP_K) -> int:
        """Return the Similarity Top-K value in the prompt."""
        context_size = self._match.group('context_size')
        top_k = default_top_k if context_size is None else int(context_size)
        return top_k

    def get_prompt(self) -> str:
        """Return the actual prompt text."""
        return self._match.group('prompt')