import discord
from discord.commands import Option
from discord.ext import commands

from bot import bot, db, testing_guilds
from bot.enums import CensorMode

options = bot.command_group(
    "options", "Change bot settings for your server", guild_ids=testing_guilds
)

whitelist = options.command_group(
    "whitelist", "Set certain words to be ignored by the censoring engine"
)


@options.command()
@commands.has_guild_permissions(administrator=True)
async def enable(ctx: discord.ApplicationContext):
    """
    Enable censoring features
    """

    await db.set_guild_option(ctx.guild_id, "enabled", True)
    await ctx.respond("Censoring has been **enabled**!")


@options.command()
@commands.has_guild_permissions(administrator=True)
async def disable(ctx: discord.ApplicationContext):
    """
    Disable censoring features
    """

    await db.set_guild_option(ctx.guild_id, "enabled", False)
    await ctx.respond("Censoring has been **disabled**!")


@options.command(name="character")
@commands.has_guild_permissions(manage_messages=True)
async def set_censor_char(ctx: discord.ApplicationContext, character: str):
    """
    Set the character which replaces profanities in messages, only applicable for Normal mode
    """

    if len(character) > 1:
        await ctx.respond("`character` parameter must be 1 character long")
        return

    await db.set_guild_option(ctx.guild_id, "censor_char", character)
    await ctx.respond(f"Censor character has been set to {character}")


@options.command(name="mode")
@commands.has_guild_permissions(manage_messages=True)
async def set_censor_mode(
    ctx: discord.ApplicationContext,
    mode: Option(
        str,
        choices=[m.name for m in CensorMode],
    ),
):
    """
    Set the method of censoring
    """

    await db.set_guild_option(ctx.guild_id, "censor_mode", mode)
    mode_embed = discord.Embed(
        title=f"Censor Mode: {mode.capitalize()}",
        color=discord.Color.red(),
        description=f"{CensorMode[mode].value}",
    )
    await ctx.respond(embed=mode_embed)


@whitelist.command(name="add")
@commands.has_guild_permissions(manage_messages=True)
async def whitelist_add(ctx: discord.ApplicationContext, word: str):
    """
    Add a word to the whitelist
    """

    guild_whitelist = (await db.get_guild_options(ctx.guild_id)).whitelist
    word = word.replace("`", "")

    if word in guild_whitelist:
        await ctx.respond(f"`{word}` is already added to the whitelist")
        return

    guild_whitelist.append(word)
    await db.set_guild_option(ctx.guild_id, "whitelist", guild_whitelist)
    await ctx.respond(f"`{word}` has been added to the whitelist")


@whitelist.command(name="remove")
@commands.has_guild_permissions(manage_messages=True)
async def whitelist_remove(ctx: discord.ApplicationContext, word: str):
    """
    Remove a word from the whitelist
    """

    guild_whitelist = (await db.get_guild_options(ctx.guild_id)).whitelist
    word = word.replace("`", "")

    if word not in guild_whitelist:
        await ctx.respond(f"`{word}` is not in the whitelist")
        return

    guild_whitelist.remove(word)
    await db.set_guild_option(ctx.guild_id, "whitelist", guild_whitelist)
    await ctx.respond(f"`{word}` has been removed from the whitelist")
