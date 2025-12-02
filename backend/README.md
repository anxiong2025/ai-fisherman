# AI Fisherman Backend

RAG-powered backend API for AI Fisherman.

## Features

- FastAPI web framework
- RAG (Retrieval Augmented Generation) for content search
- Multiple LLM providers: OpenAI, Anthropic, Gemini
- Local embedding model (sentence-transformers)
- ChromaDB vector store
- OAuth authentication (GitHub, Google)
- Article management API

## Setup

```bash
# Install dependencies
uv sync

# Copy environment file
cp .env.example .env

# Run development server
uv run fastapi dev app/main.py
```

## Configuration

Edit `.env` to configure:
- `LLM_PROVIDER`: Choose between `openai`, `anthropic`, or `gemini`
- OAuth credentials for GitHub/Google login
- API keys for your chosen LLM provider
