from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, GEMINI_API_KEY
from providers import GeminiProvider


dp = Dispatcher()
provider = GeminiProvider(GEMINI_API_KEY)

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created with aiogram.")

@dp.message()
async def message_handler(message: Message) -> None:
    reply = await provider.generate(message.text)
    await message.answer(reply)

async def start_bot() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)
