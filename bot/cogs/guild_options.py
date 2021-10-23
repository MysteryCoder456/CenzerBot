import discord
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


def setup(bot: commands.Bot):
    bot.add_cog(GuildOptions(bot))
