from sqlalchemy import Column, Integer, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

# Base class which all models derive from
Base = declarative_base()


class Options(Base):
    __tablename__ = "options"

    guild_id = Column("guild_id", Integer, primary_key=True)
    hard_censor = Column("hard_censor", Boolean, default=False, nullable=False)
    whitelist = Column("whitelist", JSON, default=[], nullable=False)

    def __repr__(self) -> str:
        return f"Options(guild_id={self.guild_id})"
