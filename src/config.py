"""Application settings.
"""

import os

LOG_FORMAT: str = os.getenv(
    'LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
"""Format for the logs displayed by the application."""

OLLAMA_HOST: str = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
"""Host of the Ollama server."""

OLLAMA_REQUEST_TIMEOUT: float = float(os.getenv('LLM_TIMEOUT', '600.0'))
"""Request timeout to the Ollama server."""

OPEN_ROUTER_HOST: str = os.getenv(
    'OPEN_ROUTER_HOST', 'https://openrouter.ai/api/v1/chat/completions')
"""Host of the OpenRouter API."""

OPEN_ROUTER_KEY: str = os.getenv(
    'OPEN_ROUTER_KEY', '<Replace with your key>')
"""Key of the OpenRouter API."""

MODEL_GENERATOR: str = os.getenv('MODEL_GENERATOR', 'OLLAMA')
"""Generator used for LLM generation (OLLAMA, OPENROUTER). Defaults to OLLAMA."""

MODEL_EMBEDDINGS: str = os.getenv('MODEL_EMBEDDINGS', 'nomic-embed-text')
"""Name of the embedding model used by the application."""

MODEL_LLM: str = os.getenv('MODEL_LLM', 'contextualized_assistant')
"""Name of the LLM model used by the application."""

VECTOR_DB_PATH: str = os.getenv('VECTOR_DB_PATH', './.data/vdb')
"""Path where the embeddings data will be saved."""

SESSION_PATH: str = os.getenv('SESSION_PATH', './.data/session')
"""Directory where session files are stored."""
