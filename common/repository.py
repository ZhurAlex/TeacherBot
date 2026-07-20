from sqlalchemy import select
from common.models import User, Message
from config import async_session

async def get_or_create_user(
        chat_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) ->User:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.chat_id == chat_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(
                chat_id=chat_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user
    
async def get_all_users() -> list[User]:
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
    
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