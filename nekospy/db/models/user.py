from sqlalchemy import Column, Integer, select
from nekospy.db.base import Base
from nekospy.db.session import get_session_direct

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    topic_id = Column(Integer)

    @classmethod
    async def _get_session(cls):
        return await get_session_direct()

    @classmethod
    async def add_user(cls, telegram_id: int, topic_id: int):
        session = await cls._get_session()
        user = cls(telegram_id=telegram_id, topic_id=topic_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        await session.close()
        return user

    @classmethod
    async def get(cls, user_id: int):
        session = await cls._get_session()
        result = await session.execute(select(cls).where(cls.telegram_id == user_id))
        user = result.scalar_one_or_none()
        await session.close()
        return user