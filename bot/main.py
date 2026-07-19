import asyncio
from bot.handlers import start_bot
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

if __name__ == "__main__":
    asyncio.run(start_bot())
          