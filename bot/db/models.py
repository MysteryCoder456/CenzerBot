from sqlalchemy import Column, Integer, Boolean, JSON, Text, CHAR
from sqlalchemy.ext.declarative import declarative_base

# Base class which all models derive from
Base = declarative_base()


class Options(Base):
    __tablename__ = "options"

    id = Column("id", Integer, primary_key=True)  # Guild ID
    enabled = Column("enabled", Boolean, default=True, nullable=False)
    censor_char = Column("censor_char", CHAR, default="-", nullable=False)
    hard_censor = Column("hard_censor", Boolean, default=False, nullable=False)
    whitelist = Column("whitelist", JSON, default=[], nullable=False)

    def __repr__(self) -> str:
        return f"Options(guild_id={self.guild_id})"


class Webhooks(Base):
    __tablename__ = "webhooks"

    id = Column("id", Integer, primary_key=True)  # Channel ID
    url = Column("url", Text, nullable=False)

    def __repr__(self) -> str:
        return f"Webhook(channel={self.channel_id}, url={self.url})"
