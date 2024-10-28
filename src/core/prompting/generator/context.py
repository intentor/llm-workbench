"""Context generation module."""

from core.prompting.base import GeneratedResponse, Prompt, ResponseGenerator
from core.prompting.indexer import ContextIndexer

PARAM_TOP_K = 'top-k'
PARAM_FILE_NAME = 'file'
DEFULT_TOP_K: int = 10


class ContextResponseGenerator(ResponseGenerator):
    """Generate responses from indexed context."""

    def __init__(
        self,
            indexer: ContextIndexer
    ):
        """
        Args:
            - indexer: Index manager
        """
        self._indexer = indexer

    def get_type(self) -> str:
        return 'context'

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        params = prompt.get_generator_parameters()
        param_top_k = int(params[PARAM_TOP_K]
                          ) if PARAM_TOP_K in params else DEFULT_TOP_K
        param_file_name = params[PARAM_FILE_NAME] if PARAM_FILE_NAME in params else ''

        response = self._indexer.query(
            prompt.get_prompt(),
            param_top_k,
            param_file_name)

        return GeneratedResponse(
            value=response
        )
