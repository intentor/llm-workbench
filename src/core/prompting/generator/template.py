"""Template generation module."""

from logging import getLogger
import json

import jinja2

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator
from core.prompting.history import PromptHistory

logger = getLogger()


class TemplateResponseGenerator(ResponseGenerator):
    """Apply the last response as JSON in a template defined by the prompt.."""

    def __init__(
        self,
        history: PromptHistory,
    ):
        """
        Args:
            - history: Prompt history manager.
        """
        self._history = history

    def get_type(self) -> str:
        return 'template'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        template_format = prompt.get_prompt()

        try:
            last_response = self._history.get_last_response()
            data = json.loads(last_response)
            context = {"context": data}

            environment = jinja2.Environment(
                extensions=['jinja2_iso8601.ISO8601Extension'])
            template = environment.from_string(template_format)
            response = template.render(context)
        except Exception as e:
            logger.error('m=generate type=template  e=%s', e)
            response = ('Could not apply the last response to the template. '
                        'Please check the previous response and try again.')

        return GeneratedResponse(
            value=response
        )
