from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = getenv("MISTRAL_API_KEY")

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

_required = {
    'BOT_TOKEN': BOT_TOKEN,
    'GEMINI_API_KEY': GEMINI_API_KEY,
    'MISTRAL_API_KEY': MISTRAL_API_KEY,
    'POSTGRES_USER': POSTGRES_USER,
    'POSTGRES_PASSWORD': POSTGRES_PASSWORD,
    'POSTGRES_DB': POSTGRES_DB,
}

_missing = [ name for name, value in _required.items() if not value]
if _missing:
    raise ValueError(f"Environment variables are missing: {', '.join(_missing)}. Please check .env file")