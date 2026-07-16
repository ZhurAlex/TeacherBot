from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = getenv("MISTRAL_API_KEY")

_required = {
    'BOT_TOKEN': BOT_TOKEN,
    'GEMINI_API_KEY': GEMINI_API_KEY,
    'MISTRAL_API_KEY': MISTRAL_API_KEY,
}

_missing = [ name for name, value in _required.items() if not value]
if _missing:
    raise ValueError(f"Environment variables are missing: {', '.join(_missing)}. Please check .env file")