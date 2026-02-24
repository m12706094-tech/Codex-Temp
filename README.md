# Ollama DeepSeek Backend

A clean and minimal Python backend using **FastAPI + LangChain + Ollama** with
`deepseek-r1:1.5b`.

## Design principles

- **KISS**: two endpoints only (`/health`, `/chat`).
- **DRY**: all provider settings live in one config class.
- **Clean code**: API layer, schema layer, and LLM layer are separated.

## Project structure

- `app/config.py` → environment-driven Ollama settings
- `app/llm_service.py` → LangChain/Ollama integration
- `app/schemas.py` → request/response models
- `app/main.py` → FastAPI app and routes
- `tests/test_api.py` → API tests with dependency overrides

## 1) Prerequisites

- Python 3.10+
- Ollama running locally

```bash
ollama pull deepseek-r1:1.5b
```

## 2) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Optional environment variables

All variables are prefixed with `OLLAMA_`:

- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `OLLAMA_MODEL` (default: `deepseek-r1:1.5b`)
- `OLLAMA_TEMPERATURE` (default: `0.2`)

Example:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=deepseek-r1:1.5b
export OLLAMA_TEMPERATURE=0.1
```

## 4) Run backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 5) API usage

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain recursion simply."}'
```

Response shape:

```json
{
  "answer": "...",
  "model": "deepseek-r1:1.5b"
}
```
