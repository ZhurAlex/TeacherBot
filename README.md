# TeacherBot

A Telegram bot that helps with grammar, spelling, and punctuation — powered by LLMs, with automatic fallback between providers. Works in any language: it replies in whichever language the question was asked in.

## Features

- Answers grammar, spelling, and punctuation questions, automatically replying in the same language as the question
- Automatic fallback across multiple LLM providers — if one fails or hits a rate limit, the bot transparently retries with the next
- Handles Telegram's 4096-character message limit by splitting long responses
- Fully async (aiogram + async LLM clients), no blocking calls in the event loop

## Architecture

The project follows a simplified **ports and adapters** approach for the LLM layer:

- **`LLMProvider`** (port) — an abstract base class defining a single contract: `generate(text, system) -> str`
- **`GeminiProvider`**, **`MistralProvider`** (adapters) — concrete implementations wrapping the Google Gemini and Mistral AI SDKs behind that same contract
- **`FallbackProvider`** — composes a list of providers and tries them in order, falling back to the next one on failure

This means the bot's core logic never talks to a specific LLM SDK directly — it only depends on the `LLMProvider` interface. Adding a new provider (e.g. Claude, Groq) means writing one new adapter class; no changes needed anywhere else.

```
Telegram message
      │
      ▼
 aiogram handler
      │
      ▼
FallbackProvider.generate()
      │
      ├─► GeminiProvider   (tried first)
      │
      └─► MistralProvider  (tried if Gemini fails)
```

## Tech stack

- **Python 3.14**, [Poetry](https://python-poetry.org/) for dependency management
- [aiogram 3.x](https://docs.aiogram.dev/) — async Telegram Bot framework
- [google-genai](https://github.com/googleapis/python-genai) — Gemini API client
- [mistralai](https://github.com/mistralai/client-python) — Mistral AI client
- `python-dotenv` for configuration

## Project structure

```
TeacherBot/
├── bot/
│   ├── main.py          # entry point
│   ├── handlers.py       # aiogram dispatcher, handlers
│   ├── prompts.py        # system prompt
│   └── providers.py      # LLMProvider interface + Gemini/Mistral/Fallback adapters
├── admin/                # FastAPI admin panel
│   ├── main.py           # app entry point, CORS
│   ├── routes.py         # /users endpoints (list, detail, messages, block)
│   ├── schemas.py        # Pydantic response models
│   └── frontend/         # React + TypeScript admin UI (Vite, TanStack Query)
├── common/
│   ├── models.py         # SQLAlchemy models
│   └── repository/
│       ├── users.py      # user queries
│       └── messages.py   # message queries
├── config/               # environment variable loading & validation
├── alembic/              # database migrations
├── .env.example          # required environment variables (no secrets)
└── pyproject.toml        # dependencies (Poetry)
```

## Setup

```bash
git clone git@github.com:ZhurAlex/TeacherBot.git
cd TeacherBot

poetry install

cp .env.example .env
# fill in BOT_TOKEN, GEMINI_API_KEY, MISTRAL_API_KEY

poetry run python -m bot.main
```

### Admin panel

```bash
# backend (from repo root)
poetry run uvicorn admin.main:app --port 8000

# frontend (in another terminal)
cd admin/frontend
npm install
cp .env.example .env   # set VITE_API_BASE_URL if the backend isn't on localhost:8000
npm run dev
```

The frontend runs on `http://localhost:5173` and expects the backend at `http://localhost:8000` (already allowed via CORS in `admin/main.py`).

## Roadmap

- [x] **Stage 1 — MVP bot**: forward user questions to an LLM with fallback between providers
- [x] **Stage 2 — Admin panel**: FastAPI backend + React frontend for viewing users and usage, blocking abusive accounts
- [ ] **Stage 3 — RAG on personal error history**: track each user's recurring mistakes and surface relevant past examples via semantic search
- [ ] **Stage 4 — Admin panel hardening**: JWT authorization, automated tests, and a chart of daily request volume
