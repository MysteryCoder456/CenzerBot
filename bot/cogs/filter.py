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
        if message.author == self.bot.user:
            return

        channel: discord.TextChannel = message.channel
        message_split: List[str] = message.content.split()
        filter_character = "-"
        clean_sentence_list = []

        for word in message_split:
            clean_word = word
            for profanity in self.profanity_words:
                if profanity in word:
                    clean_word = filter_character * len(word)
            clean_sentence_list.append(clean_word)

        clean_sentence = " ".join(clean_sentence_list)
        await channel.send(f"Clean sentence: {clean_sentence}")


def setup(bot: commands.Bot):
    bot.add_cog(Filter(bot))
