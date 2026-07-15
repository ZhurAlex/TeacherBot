from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")