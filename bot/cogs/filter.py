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
        self.profanity_words = words_request.text.splitlines()
        print("Fetched profanities 😉")

    async def get_channel_webhook(self, channel: discord.TextChannel) -> discord.Webhook:
        channel_webhooks = await channel.webhooks()
        bot_webhook: discord.Webhook | None = discord.utils.get(channel_webhooks, user=self.bot.user)

        if bot_webhook is None:
            bot_webhook = await channel.create_webhook(name=f"Cenzer Webhook", reason="Used to replace profanity messages with censored ones")

        return bot_webhook

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
                channel_webhook = await self.get_channel_webhook(channel)
                clean_sentence_list = []
                contains_profanity = False

                for word in message.content.split():
                    clean_word = word
                    for profanity in self.profanity_words:
                        if profanity in word.lower():
                            contains_profanity = True
                            clean_word = options.censor_char * len(word)
                    clean_sentence_list.append(clean_word)

                if contains_profanity:
                    clean_sentence = " ".join(clean_sentence_list)
                    name = message.author.display_name
                    avatar = message.author.avatar_url  # type: ignore

                    await message.delete()
                    await channel_webhook.send(clean_sentence, username=name, avatar_url=avatar)

            # Deleting messages that contain any profanities
            case CensorMode.delete:
                contains_profanity = False

                for word in message.content.split():
                    for profanity in self.profanity_words:
                        if profanity in word.lower():
                            contains_profanity = True
                            break
                    if contains_profanity:
                        break

                if contains_profanity:
                    await message.delete()

            # Wrap profanities in spoiler tags
            case CensorMode.spoiler:
                # TODO: Make this
                pass


def setup(bot: commands.Bot):
    bot.add_cog(Filter(bot))
