"""FastAPI backend using Ollama + deepseek-r1:1.5b via LangChain."""

from fastapi import Depends, FastAPI, HTTPException

from app.config import OllamaConfig
from app.llm_service import LLMService, LLMServiceError
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="Ollama DeepSeek Backend", version="1.1.0")

config = OllamaConfig()
llm_service = LLMService(config)


def get_llm_service() -> LLMService:
    """Dependency injection hook for testability."""

    return llm_service


@app.get("/health")
def health(service: LLMService = Depends(get_llm_service)) -> dict[str, str]:
    """Simple health check endpoint."""

    return {"status": "ok", "model": service.model_name}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, service: LLMService = Depends(get_llm_service)) -> ChatResponse:
    """Generate a response for a user prompt."""

    try:
        answer = service.ask(payload.prompt)
        return ChatResponse(answer=answer, model=service.model_name)
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}") from exc
