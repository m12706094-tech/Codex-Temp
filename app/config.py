"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OllamaConfig(BaseSettings):
    """Settings for the Ollama model endpoint."""

    model_config = SettingsConfigDict(env_prefix="OLLAMA_", env_file=".env", extra="ignore")

    base_url: str = Field(default="http://localhost:11434")
    model: str = Field(default="deepseek-r1:1.5b")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
