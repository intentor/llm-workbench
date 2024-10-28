"""Application settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    """Format for the logs displayed by the application."""

    ollama_host: str = 'http://localhost:11434'
    """Host of the Ollama server."""

    ollama_request_timeout: int = 600
    """Request timeout to the Ollama server, in seconds."""

    ollama_model: str = 'contextualized-assistant'
    """Name of the LLM model used by Ollama."""

    open_router_host: str = 'https://openrouter.ai/api/v1/chat/completions'
    """Host of the OpenRouter API."""

    open_router_key: str
    """App key of the OpenRouter API."""

    open_router_request_timeout: int = 60000
    """Request timeout to the OpenRouter server, in miliseconds."""

    open_router_model: str = 'contextualized-assistant'
    """Name of the LLM model used by OpenRouter."""

    model_gateway: str = 'OLLAMA'
    """Gateway used for LLM generation (OLLAMA, OPENROUTER). Defaults to OLLAMA."""

    model_embeddings: str = 'mxbai-embed-large'
    """Name of the embedding model used by the application."""

    vector_db_path: str = './.data/vdb'
    """Path where the embeddings data will be saved."""

    session_path: str = './.data/session'
    """Directory where session files are stored."""

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_settings() -> Settings:
    return Settings()
