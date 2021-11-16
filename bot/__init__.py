import os
import sys
import importlib
import asyncio
import discord
from dotenv import load_dotenv

from bot import db

load_dotenv()
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.messages = True
testing_guilds = (
    list(map(int, os.environ["TESTING_GUILDS"].split(",")))
    if "--debug" in sys.argv
    else None
)
bot = discord.Bot(
    description=(
        "I am a bot that will censor most (if not all) bad words in your "
        "sentences without deleting your messages."
    ),
    intents=intents,
)


@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    print(f"Logged in as {bot.user} in {guild_count} guilds")


@bot.slash_command(guild_ids=testing_guilds)
async def invite(ctx: discord.ApplicationContext):
    """
    Get Cenzer's invite link
    """

    invite_url = "https://discord.com/api/oauth2/authorize?client_id=871480702640726077&permissions=105763578896&scope=bot%20applications.commands"
    invite_embed = discord.Embed(
        title="Invite Cenzer to your server",
        description="Thank you for spreading the word",
        url=invite_url,
        color=discord.Color.red(),
    )
    await ctx.respond(embed=invite_embed)


def load_commands():
    commands_dir = ["bot", "commands"]
    commands_module = ".".join(commands_dir)

    for filename in os.listdir("/".join(commands_dir)):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            importlib.import_module(f"{commands_module}.{module_name}")
            print(f"Loaded {module_name} module")


def main():
    loop = asyncio.get_event_loop()
    try:
        load_commands()
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
