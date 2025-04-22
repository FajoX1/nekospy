import asyncio
from .models import user
from nekospy.db.base import Base
from nekospy.db.session import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

user = user.User