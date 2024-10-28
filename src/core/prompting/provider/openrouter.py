"""OpenRouter generation module."""

import json
import requests

from core.prompting.base import (
    GeneratedResponse,
    GenerationError,
    ModelProvider
)


class OpenRouterModelProvider(ModelProvider):
    """Generate responses from an LLM using OpenRouter."""

    def __init__(
        self,
            api_url: str,
            api_key: str,
            api_timeout: int = 6000,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - api_url: OpenRouter's API endpoint.
            - api_key: OpenRouter's API key.
            - api_timeout: OpenRouter's API timeout.
            - model_name: Name of the LLM model used for generation.
        """
        self._api_url = api_url
        self._api_key = api_key
        self._api_timeout = api_timeout
        self._model_name = model_name

    def generate(self, prompt: str) -> GeneratedResponse:
        try:
            response = requests.post(
                url=self._api_url,
                timeout=self._api_timeout,
                headers={
                    'Authorization': f"Bearer {self._api_key}"
                },
                data=json.dumps({
                    'model': self._model_name,
                    'messages': [
                        {
                            'role': "user",
                            'content': prompt
                        }
                    ]
                })
            )
        except Exception as ex:
            raise GenerationError(
                'Cannot perform request to OpenRouter') from ex

        status_code: int = response.status_code
        if status_code == 200:
            api_response = response.json()

            if 'error' in api_response:
                raise GenerationError(
                    f"OpenRouter HTTP request error: {api_response['error']}")

            generated_response = GeneratedResponse(
                value=api_response['choices'][0]['message']['content'],
                input_tokens=api_response['usage']['prompt_tokens'],
                output_tokens=api_response['usage']['completion_tokens']
            )

            return generated_response
        else:
            raise GenerationError(
                f"OpenRouter HTTP request error: {status_code}")
