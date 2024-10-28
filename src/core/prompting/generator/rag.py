"""RAG generation module."""

from logging import getLogger

from core.prompting.base import GeneratedResponse, Prompt
from core.prompting.generator.context import ContextResponseGenerator
from core.prompting.generator.model import ModelResponseGenerator
from core.prompting.history import HistoryAwareResponseGeneator, PromptHistory

logger = getLogger()


class RagResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses querying the context and passing it to a model.

    This is a shortcut generator which operates other generators, so no 
    history for /rag is created.
    """

    def __init__(
        self,
            history: PromptHistory,
            model_generator: ModelResponseGenerator,
            context_generator: ContextResponseGenerator
    ):
        """
        Args:
            - history: Prompt history manager.
            - ollama_generator: Ollama generator.
            - context_generator: Context generator.
        """
        super().__init__(history)
        self._model_generator = model_generator
        self._context_generator = context_generator

    def get_type(self) -> str:
        return 'rag'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())

        context_query = '/context ' + prompt.get_prompt()
        context_response = self._context_generator.generate(
            Prompt(context_query)
        )

        gateway_query = f"""Context information is below:
---------------------
{context_response.value}
---------------------

Given the context information and no prior knowledge, answer the query.
Query: {prompt_text}
Answer:
"""

        generated_response = self._model_generator.generate(
            Prompt(gateway_query)
        )

        logger.debug('m=generate type=rag prompt=%s response=%s',
                     prompt_text, generated_response)

        return generated_response
