"""LLM service layer."""

from langchain_ollama import ChatOllama

from app.config import OllamaConfig


class LLMServiceError(RuntimeError):
    """Raised when the LLM provider fails."""


class LLMService:
    """Handles interaction with Ollama through LangChain."""

    def __init__(self, config: OllamaConfig) -> None:
        self._model_name = config.model
        self._client = ChatOllama(
            model=config.model,
            base_url=config.base_url,
            temperature=config.temperature,
        )

    @property
    def model_name(self) -> str:
        """Configured model name."""

        return self._model_name

    def ask(self, prompt: str) -> str:
        """Get an answer from the configured model."""

        try:
            response = self._client.invoke(prompt)
        except Exception as exc:  # pragma: no cover - runtime integration safety
            raise LLMServiceError(str(exc)) from exc

        content = response.content
        return content if isinstance(content, str) else str(content)
