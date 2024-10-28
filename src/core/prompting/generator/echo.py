"""Echo generation module."""

from core.prompting.base import GeneratedResponse, Prompt
from core.prompting.history import HistoryAwareResponseGeneator


class EchoResponseGenerator(HistoryAwareResponseGeneator):
    """Generate the exact same prompt but with replacements."""

    def get_type(self) -> str:
        return 'echo'

    def generate(self, prompt: Prompt) -> str:
        response = self._replacer.replace(prompt.get_prompt())

        generated_response = GeneratedResponse(
            value=response
        )
        self._append_history(prompt, generated_response)

        return generated_response
