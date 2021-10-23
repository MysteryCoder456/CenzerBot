import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.db.models import Base, Options

# SQLAlchemy Engine
load_dotenv()
uri = os.environ["DB_URI"]
engine = create_async_engine(uri)


async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close():
    await engine.dispose()


async def get_guild_options(guild_id: int) -> Options:
    guild_options: Options

    async with AsyncSession(engine) as session:
        guild_options = await session.get(Options, guild_id)

        if guild_options is None:
            new_options = Options(id=guild_id)
            session.add(new_options)
            await session.commit()

            guild_options = await session.get(Options, guild_id)

    return guild_options
