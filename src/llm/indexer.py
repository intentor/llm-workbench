"""Manages indexing of files in a vector database."""


from typing import List
from logging import getLogger

logger = getLogger()


class ContextIndexer():
    """Manages indexing files."""

    def __init__(self, vdb_path: str):
        """
        Args:
            - vdb_path: Path to the data of the vector database.
        """
        self._vdb_path = vdb_path

    def index_files(self, files_path: List[str]):
        """Index files in the context.

        Args:
            - files_path: Path of each file to be indexed.
        """

        logger.info('m=index files=%s', files_path)
        return

    def query(self, prompt: str) -> str:
        """Query the context.

        Args:
            - prompt: Prompt to query the context.

        Returns:
            Context found or empty string.
        """

        logger.info('m=query prompt=%s', prompt)
        return f"Context.\n{prompt}"
