from sqlalchemy import select, func
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

async def get_user_by_id(user_id: int) -> User | None:
    async with async_session() as session:
        result = await session.execute(select(User, func.sum(Message.tokens_used).label("total_tokens"))
                                       .outerjoin(Message, User.id == Message.user_id)
                                       .where(User.id == user_id)
                                       .group_by(User.id))
        row = result.first()
        if row is None:
            return None
        user, total_tokens = row
        user.total_tokens = total_tokens or 0
        
        return user

async def get_all_users() -> list[User]:
    async with async_session() as session:
        result = await session.execute(select(User, func.sum(Message.tokens_used).label("total_tokens"))
                                              .outerjoin(Message, User.id == Message.user_id)
                                              .group_by(User.id)
                                              .order_by(User.id))
        users = []
        for user, total_tokens in result.all():
            user.total_tokens = total_tokens or 0
            users.append(user)

        return users
