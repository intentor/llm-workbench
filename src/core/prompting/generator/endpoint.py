"""Endpoint generation module."""

import requests

from core.prompting.base import GeneratedResponse, Prompt
from core.prompting.history import HistoryAwareResponseGeneator

PARAM_URL = 'url'


class EndpointResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from endpoints."""

    def get_type(self) -> str:
        return 'endpoint'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        url = prompt.get_prompt()

        if url is None:
            raise ValueError('No URL was provided.')

        response = requests.get(url, timeout=60)
        contents = response.text

        generated_response = GeneratedResponse(
            value=contents
        )
        self._append_history(prompt, generated_response)

        return generated_response
