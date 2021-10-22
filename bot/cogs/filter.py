from typing import List
import requests
import discord
from discord.ext import commands

from bot import db
from bot.enums import CensorMode


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
        if message.author.bot:  # type: ignore
            return

        channel: discord.TextChannel = message.channel
        guild_id: int = channel.guild.id
        options = db.get_guild_options(guild_id)

        if not options.enabled:
            return

        match options.censor_mode:
            # Replacing profanities with the censor character
            case CensorMode.normal:
                # TODO: Use webhooks to send censored version
                clean_sentence_list = []

                for word in message.content.split():
                    clean_word = word
                    for profanity in self.profanity_words:
                        if profanity in word:
                            clean_word = options.censor_char * len(word)
                    clean_sentence_list.append(clean_word)

                clean_sentence = " ".join(clean_sentence_list)
                await channel.send(f"Clean sentence: {clean_sentence}")

            # Deleting messages that contain any profanities
            case CensorMode.delete:
                contain_profanity = False

                for word in message.content.split():
                    for profanity in self.profanity_words:
                        if profanity in word:
                            contain_profanity = True
                            break
                    if contain_profanity:
                        break

                if contain_profanity:
                    await message.delete()

            # Wrap profanities in spoiler tags
            case CensorMode.spoiler:
                # TODO: Make this
                pass


def setup(bot: commands.Bot):
    bot.add_cog(Filter(bot))
