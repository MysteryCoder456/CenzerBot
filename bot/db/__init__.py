import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bot.db.models import Base, Options

# SQLAlchemy Engine
uri = os.environ["DB_URI"]
engine = create_engine(uri)

# Create tables
Base.metadata.create_all(bind=engine)


def get_guild_options(guild_id: int) -> Options:
    guild_options: Options

    with Session(engine) as session:  # type: ignore
        guild_options = session.query(Options).filter_by(id=guild_id).scalar()

        if guild_options is None:
            new_options = Options(id=guild_id)
            session.add(new_options)
            session.commit()

            guild_options = (
                session.query(Options).filter_by(id=guild_id).scalar()
            )

    return guild_options
