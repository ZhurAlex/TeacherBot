from sqlalchemy import select
from common.models import User, Message
from config import async_session

async def get_user_messages(user_id: int) -> list[Message] | None:
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user is None:
            return None
        result = await session.execute(select(Message).where(Message.user_id == user_id))
        messages = result.scalars().all()
        return messages

async def save_message(user: User, text: str, response: str, provider_used: str, tokens_used: int | None = None) -> Message:
    async with async_session() as session:
        message = Message(
            user_id=user.id,
            text=text,
            response=response,
            provider_used=provider_used,
            tokens_used=tokens_used
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message
