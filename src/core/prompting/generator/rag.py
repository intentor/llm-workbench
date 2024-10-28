"""RAG generation module."""

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator
from core.prompting.generator.context import ContextResponseGenerator
from core.prompting.generator.model import ModelResponseGenerator


class RagResponseGenerator(ResponseGenerator):
    """Generate responses querying the context and passing it to a model.

    This is a shortcut generator which operates other generators, so no 
    history for /rag is created.
    """

    def __init__(
        self,
            model_generator: ModelResponseGenerator,
            context_generator: ContextResponseGenerator
    ):
        """
        Args:
            - ollama_generator: Ollama generator.
            - context_generator: Context generator.
        """
        self._model_generator = model_generator
        self._context_generator = context_generator

    def get_type(self) -> str:
        return 'rag'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        context_query = '/context ' + prompt.get_prompt()
        context_response = self._context_generator.generate(
            Prompt(context_query)
        )

        rag_prompt = f"""Context information is below:
---------------------
{context_response.value}
---------------------

Given the context information and no prior knowledge, answer the query.
Query: {prompt.get_prompt()}
Answer:
"""

        return self._model_generator.generate(
            Prompt(rag_prompt)
        )
