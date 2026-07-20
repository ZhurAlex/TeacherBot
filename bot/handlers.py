from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, GEMINI_API_KEY, MISTRAL_API_KEY
from bot.providers import GeminiProvider, MistralProvider, FallbackProvider
from bot.prompts import SYSTEM_PROMPT
from common.models import User
from common.repository import get_or_create_user, save_message

TELEGRAM_MESSAGE_LIMIT = 4096

dp = Dispatcher()
provider = FallbackProvider([GeminiProvider(GEMINI_API_KEY), MistralProvider(MISTRAL_API_KEY)])

async def check_user(message: Message) -> User:
    return await get_or_create_user(
        chat_id=message.chat.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        "I help with grammar, spelling, and punctuation questions. "
        "Ask me anything about how a word is spelled, where a comma goes, "
        "or why a sentence sounds off — I'll explain the rule and give an example.\n\n"
        "I reply in whichever language you write to me in."
    )

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await check_user(message)
    await message.answer("Hello! I'm a bot created with aiogram.")

@dp.message()
async def message_handler(message: Message) -> None:
    if not message.text:
        await message.answer("Please send a text message.")
        return
    user = await check_user(message)
    reply = await provider.generate(message.text, SYSTEM_PROMPT)

    await send_response(message, reply.text)
    await save_message(user, message.text, reply.text, reply.provider_name, reply.tokens_used)

async def send_response(message: Message, text: str):
    if len(text) <= TELEGRAM_MESSAGE_LIMIT:
        await message.answer(text)
    else:
        for i in range(0, len(text), TELEGRAM_MESSAGE_LIMIT):
            await message.answer(text[i:i + TELEGRAM_MESSAGE_LIMIT])

async def start_bot() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)
