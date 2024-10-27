"""OpenRouter generation module."""

from logging import getLogger
import json
import requests

from core.prompting.base import (
    DEFULT_GENERATOR_TYPE,
    GeneratedResponse,
    GenerationError,
    Prompt
)
from core.prompting.history import HistoryAwareResponseGeneator, PromptHistory

logger = getLogger()


class OpenRouterResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from an LLM using OpenRouter."""

    def __init__(
        self,
            history: PromptHistory,
            api_url: str,
            api_key: str,
            api_timeout: int = 6000,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - history: Prompt history manager.
            - api_url: OpenRouter's API endpoint.
            - api_key: OpenRouter's API key.
            - api_timeout: OpenRouter's API timeout.
            - model_name: Name of the LLM model used for generation.
        """
        super().__init__(history)
        self._api_url = api_url
        self._api_key = api_key
        self._api_timeout = api_timeout
        self._model_name = model_name

    def get_type(self) -> str:
        return DEFULT_GENERATOR_TYPE

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())

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
                            'content': prompt_text
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

            logger.debug('m=generate type=openrouter api_response=%s',
                         api_response)

            if 'error' in api_response:
                raise GenerationError(
                    f"OpenRouter HTTP request error: {api_response['error']}")

            generated_response = GeneratedResponse(
                value=api_response['choices'][0]['message']['content'],
                input_tokens=api_response['usage']['prompt_tokens'],
                output_tokens=api_response['usage']['completion_tokens']
            )
            self._append_history(prompt, generated_response)

            logger.debug('m=generate type=openrouter prompt=%s response=%s',
                         prompt_text, generated_response)

            return generated_response
        else:
            raise GenerationError(
                f"OpenRouter HTTP request error: {status_code}")
