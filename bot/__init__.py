import os
import discord
from discord.ext import commands
from discord.ext.prettyhelp import PrettyHelp
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TOKEN"]


def get_prefix(client: commands.Bot, message: discord.Message) -> str:
    # TODO: implement custom prefixes
    return "c."


bot = commands.Bot(
    command_prefix=get_prefix,
    description=(
        "I am a bot that will censor most (if not all) bad words in your "
        "sentences without deleting your messages."
    ),
    help_command=PrettyHelp(color=discord.Color.red()),
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
    try:
        load_cogs()
        bot.run(TOKEN)
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print("Stopping...")
