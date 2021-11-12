import discord
from discord.commands import Option
from discord.ext import commands

from bot import db, testing_guilds
from bot.enums import CensorMode


class GuildOptions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(guild_ids=testing_guilds)
    @commands.has_guild_permissions(administrator=True)
    async def enable(self, ctx: discord.ApplicationContext):
        """
        Enable censoring features
        """

        await db.set_guild_option(ctx.guild.id, "enabled", True)
        await ctx.respond("Censoring has been **enabled**!")

    @commands.slash_command(guild_ids=testing_guilds)
    @commands.has_guild_permissions(administrator=True)
    async def disable(self, ctx: discord.ApplicationContext):
        """
        Disable censoring features
        """

        await db.set_guild_option(ctx.guild.id, "enabled", False)
        await ctx.respond("Censoring has been **disabled**!")

    @commands.slash_command(name="character", guild_ids=testing_guilds)
    @commands.has_guild_permissions(manage_messages=True)
    async def set_censor_char(
        self, ctx: discord.ApplicationContext, character: str
    ):
        """
        Set the character which replaces profanities in messages, only applicable for Normal mode
        """

        if len(character) > 1:
            await ctx.respond("`character` parameter must be 1 character long")
            return

        await db.set_guild_option(ctx.guild.id, "censor_char", character)
        await ctx.respond(f"Censor character has been set to {character}")

    @commands.slash_command(name="mode", guild_ids=testing_guilds)
    @commands.has_guild_permissions(manage_messages=True)
    async def set_censor_mode(
        self,
        ctx: discord.ApplicationContext,
        mode: Option(
            str,
            choices=[m.name for m in CensorMode],
        ),
    ):
        """
        Set the method of censoring
        """

        await db.set_guild_option(ctx.guild.id, "censor_mode", mode)
        mode_embed = discord.Embed(
            title=f"Censor Mode: {mode.capitalize()}",
            color=discord.Color.red(),
            description=f"{CensorMode[mode].value}",
        )
        await ctx.respond(embed=mode_embed)


def setup(bot: commands.Bot):
    bot.add_cog(GuildOptions(bot))
