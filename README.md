# Ollama DeepSeek Backend

Minimal Python backend using **FastAPI + LangChain-Ollama + Ollama** with
`deepseek-r1:1.5b`.

## Design goals

- **KISS**: only `/health` and `/chat`.
- **DRY**: one config class for all Ollama settings.
- **Clean code**: separate config, service, schemas, and API setup.

## Project structure

- `app/config.py` → environment-based Ollama settings
- `app/llm_service.py` → model integration layer
- `app/schemas.py` → request/response contracts
- `app/main.py` → app factory + route wiring
- `tests/test_api.py` → API behavior tests

## 1) Prerequisites

- Python 3.10+
- Ollama installed and running

```bash
ollama pull deepseek-r1:1.5b
```

## 2) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Configuration

All environment variables are prefixed with `OLLAMA_`:

- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `OLLAMA_MODEL` (default: `deepseek-r1:1.5b`)
- `OLLAMA_TEMPERATURE` (default: `0.2`)

Example:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=deepseek-r1:1.5b
export OLLAMA_TEMPERATURE=0.1
```

## 4) Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 5) Use API

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain recursion simply."}'
```

Response:

```json
{
  "answer": "...",
  "model": "deepseek-r1:1.5b"
}
```
