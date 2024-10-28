"""Echo generation module."""

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator


class EchoResponseGenerator(ResponseGenerator):
    """Generate the exact same prompt."""

    def get_type(self) -> str:
        return 'echo'

    def generate(self, prompt: Prompt) -> str:
        return GeneratedResponse(
            value=prompt.get_prompt()
        )
