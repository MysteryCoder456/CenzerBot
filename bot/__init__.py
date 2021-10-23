import asyncio
import os
import discord
from discord.ext import commands
from discord.ext.prettyhelp import PrettyHelp
from dotenv import load_dotenv

from bot import db

load_dotenv()
TOKEN = os.environ["TOKEN"]


def get_prefix(client: commands.Bot, message: discord.Message) -> str:
    # TODO: implement custom prefixes
    return "c."


intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix=get_prefix,
    description=(
        "I am a bot that will censor most (if not all) bad words in your "
        "sentences without deleting your messages."
    ),
    help_command=PrettyHelp(color=discord.Color.red()),
    intents=intents,
)


@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    print(f"Logged in as {bot.user} in {guild_count} guilds")


def load_cogs():
    for filename in os.listdir("bot/cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            bot.load_extension(f"bot.cogs.{cog_name}")
            print(f"Finished loading {cog_name} cog")

    print("All cogs loaded!")


def main():
    loop = asyncio.get_event_loop()
    try:
        load_cogs()
        loop.run_until_complete(db.init_tables())
        loop.run_until_complete(bot.start(TOKEN))
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        loop.run_until_complete(bot.close())
        loop.run_until_complete(db.close())
        loop.close()
        print("Stopping...")
