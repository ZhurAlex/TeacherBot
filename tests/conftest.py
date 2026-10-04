from pathlib import Path

from dotenv import load_dotenv

# Runs before any test module is collected/imported — must happen before
# `config.settings` (which reads env vars at import time) is ever pulled in by
# a test, otherwise tests could load the real .env and hit real LLM/Telegram
# APIs or the real database with real credentials.
load_dotenv(Path(__file__).parent.parent / ".env.test", override=True)
