import requests
import discord

from bot import bot, db
from bot.enums import CensorMode


# Fetch profanity list
words_request = requests.get(
    "https://github.com/RobertJGabriel/Google-profanity-words"
    "/raw/master/list.txt"
)
profanity_words = words_request.text.splitlines()
print("Fetched profanities 😉")


async def get_channel_webhook(channel: discord.TextChannel) -> discord.Webhook:
    channel_webhooks = await channel.webhooks()
    bot_webhook: discord.Webhook | None = discord.utils.get(
        channel_webhooks,
        user=bot.user,
    )

    if bot_webhook is None:
        bot_webhook = await channel.create_webhook(
            name="Cenzer Webhook",
            reason="Used to replace profanity messages with censored ones",
        )

    return bot_webhook


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    channel: discord.TextChannel = message.channel
    guild_id: int = channel.guild.id
    options = await db.get_guild_options(guild_id)

    # Do not check for whitelisted words
    adjusted_profanities = profanity_words.copy()
    for whitelisted in options.whitelist:
        try:
            adjusted_profanities.remove(whitelisted)
        except ValueError:
            pass

    if not options.enabled:
        return

    match options.censor_mode:
        # Replacing profanities with the censor character
        case CensorMode.NORMAL:
            clean_sentence_list = []
            contains_profanity = False

            for word in message.content.split():
                clean_word = word

                for profanity in adjusted_profanities:
                    if profanity in word.lower():
                        contains_profanity = True
                        clean_word = options.censor_char * len(word)
                        break

                clean_sentence_list.append(clean_word)

            if contains_profanity:
                channel_webhook = await get_channel_webhook(channel)
                clean_sentence = " ".join(clean_sentence_list)
                name = message.author.display_name
                avatar = message.author.display_avatar

                await message.delete()
                await channel_webhook.send(
                    clean_sentence,
                    username=name,
                    avatar_url=avatar,
                )

        # Deleting messages that contain any profanities
        case CensorMode.DELETE:
            contains_profanity = False

            for word in message.content.split():
                for profanity in adjusted_profanities:
                    if profanity in word.lower():
                        contains_profanity = True
                        break
                if contains_profanity:
                    break

            if contains_profanity:
                await message.delete()

        # Wrap profanities in spoiler tags
        case CensorMode.SPOILER:
            clean_sentence_list = []
            contains_profanity = False
            no_spoiler_content: str = message.content.replace("||", "")

            for word in no_spoiler_content.split():
                clean_word = word

                for profanity in adjusted_profanities:
                    if profanity in word.lower():
                        contains_profanity = True
                        clean_word = f"||{word}||"
                        break

                clean_sentence_list.append(clean_word)

            if contains_profanity:
                channel_webhook = await get_channel_webhook(channel)
                clean_sentence = " ".join(clean_sentence_list)
                name = message.author.display_name
                avatar = message.author.display_avatar

                await message.delete()
                await channel_webhook.send(
                    clean_sentence,
                    username=name,
                    avatar_url=avatar,
                )
