"""Endpoint generation module."""

import requests

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator

PARAM_URL = 'url'


class EndpointResponseGenerator(ResponseGenerator):
    """Generate responses from endpoints."""

    def get_type(self) -> str:
        return 'endpoint'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        url = prompt.get_prompt()

        if url is None:
            raise ValueError('No URL was provided.')

        response = requests.get(url, timeout=60)
        contents = response.text

        return GeneratedResponse(
            value=contents
        )
