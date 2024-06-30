"""Application settings.
"""

import os

LOG_FORMAT: str = os.getenv(
    'LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
"""Format for the logs displayed by the application."""

OLLAMA_HOST: str = os.getenv('LLM_HOST', 'http://localhost:11434')
"""Host of the Ollama server."""

OLLAMA_REQUEST_TIMEOUT: float = float(os.getenv('LLM_TIMEOUT', '300.0'))
"""Request timeout to the Ollama server."""

MODEL_NAME: str = os.getenv('MODEL_NAME', 'contextualized_assistant_llama3')
"""Name of the LLM model that should be used by the application."""

VECTOR_DB_PATH: str = os.getenv('VECTOR_DB_PATH', './.data/vdb')
"""Path where the embeddings data will be saved."""

SESSION_PATH: str = os.getenv('SESSION_PATH', './.data/session')
"""Directory where session files are stored."""
