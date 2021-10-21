from typing import List
import requests
import discord
from discord.ext import commands


class Filter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Fetch profanity list
        words_request = requests.get(
            "https://github.com/RobertJGabriel/Google-profanity-words/raw/master/list.txt"
        )
        self.profanity_words: List[str] = words_request.text.splitlines()
        print("Fetched profanities 😉")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Filter(bot))
