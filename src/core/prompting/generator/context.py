"""Context generation module."""

from logging import getLogger

from core.prompting.base import GeneratedResponse, Prompt
from core.prompting.history import HistoryAwareResponseGeneator, PromptHistory
from core.prompting.indexer import ContextIndexer

logger = getLogger()

PARAM_TOP_K = 'top-k'
PARAM_FILE_NAME = 'file'
DEFULT_TOP_K: int = 10


class ContextResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from indexed context."""

    def __init__(
        self,
            history: PromptHistory,
            indexer: ContextIndexer
    ):
        """
        Args:
            - history: Prompt history manager.
            - indexer: Index manager
        """
        super().__init__(history)
        self._indexer = indexer

    def get_type(self) -> str:
        return 'context'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())
        params = prompt.get_generator_parameters()
        param_top_k = int(params[PARAM_TOP_K]
                          ) if PARAM_TOP_K in params else DEFULT_TOP_K
        param_file_name = params[PARAM_FILE_NAME] if PARAM_FILE_NAME in params else ''

        response = self._indexer.query(
            prompt_text,
            param_top_k,
            param_file_name)

        generated_response = GeneratedResponse(
            value=response

        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=context params=%s prompt=%s response=%s',
                     params, prompt_text, generated_response)

        return generated_response
