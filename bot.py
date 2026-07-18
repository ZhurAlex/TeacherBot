from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, GEMINI_API_KEY, MISTRAL_API_KEY, async_session
from providers import GeminiProvider, MistralProvider, FallbackProvider
from models import User, Message

TELEGRAM_MESSAGE_LIMIT = 4096
SYSTEM_PROMPT = """
You are a friendly grammar and spelling teacher. Help users with questions 
about grammar, punctuation, and spelling. Always respond in the same 
language the user's question was asked in.

Always respond in the same language the user's question was asked in.
Keep answers clear, concise, and educational, with brief examples when helpful.

If a question is unrelated to grammar, spelling, punctuation, or language 
learning, politely explain that you only help with language-related questions 
and redirect the conversation back to that topic.

Do not use markdown formatting (no asterisks, bold, headers, or bullet lists). 
Write in plain conversational text, since responses are displayed in a chat 
interface that does not render markdown well.

Keep responses under 500 words.
"""

dp = Dispatcher()
provider = FallbackProvider([GeminiProvider(GEMINI_API_KEY), MistralProvider(MISTRAL_API_KEY)])

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
    async with async_session() as session:
        usr = User(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            chat_id=message.chat.id,
        )
        session.add(usr)
        await session.commit()
    await message.answer("Hello! I'm a bot created with aiogram.")

@dp.message()
async def message_handler(message: Message) -> None:
    if not message.text:
        await message.answer("Please send a text message.")
        return
    reply = await provider.generate(message.text, SYSTEM_PROMPT)
    await send_response(message, reply)

async def send_response(message: Message, text: str):
    if len(text) <= TELEGRAM_MESSAGE_LIMIT:
        await message.answer(text)
    else:
        for i in range(0, len(text), TELEGRAM_MESSAGE_LIMIT):
            await message.answer(text[i:i + TELEGRAM_MESSAGE_LIMIT])

async def start_bot() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)
