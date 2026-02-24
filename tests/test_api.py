from fastapi.testclient import TestClient

from app.llm_service import LLMServiceError
from app.main import app


class FakeLLMService:
    model_name = "deepseek-r1:1.5b"

    def __init__(self, fail: bool = False):
        self.fail = fail

    def ask(self, prompt: str) -> str:
        if self.fail:
            raise LLMServiceError("backend unavailable")
        return f"echo: {prompt}"


client = TestClient(app)
get_llm_service = app.state.get_llm_service


def test_health() -> None:
    app.dependency_overrides[get_llm_service] = lambda: FakeLLMService()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model": "deepseek-r1:1.5b"}
    app.dependency_overrides.clear()


def test_chat_success() -> None:
    app.dependency_overrides[get_llm_service] = lambda: FakeLLMService()

    response = client.post("/chat", json={"prompt": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"answer": "echo: Hello", "model": "deepseek-r1:1.5b"}
    app.dependency_overrides.clear()


def test_chat_provider_error() -> None:
    app.dependency_overrides[get_llm_service] = lambda: FakeLLMService(fail=True)

    response = client.post("/chat", json={"prompt": "Hello"})

    assert response.status_code == 502
    assert "LLM call failed" in response.json()["detail"]
    app.dependency_overrides.clear()
