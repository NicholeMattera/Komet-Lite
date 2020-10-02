import discord
from discord.ext import commands
from discord.ext.commands import Cog
import traceback
from helpers.checks import check_if_bot_manager


class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.check(check_if_bot_manager)
    @commands.command(
        name="exit", aliases=["quit", "bye", "stop", "kill", "restart", "die"]
    )
    async def _exit(self, ctx):
        """Shuts down the bot, bot manager only."""
        await ctx.send(":wave: Goodbye!")
        await self.bot.logout()

    @commands.guild_only()
    @commands.check(check_if_bot_manager)
    @commands.command(name="eval")
    async def _eval(self, ctx):
        await ctx.send("Fuck off. This doesn't belong in production code!")

    @commands.guild_only()
    @commands.check(check_if_bot_manager)
    @commands.command()
    async def pull(self, ctx, auto=False):
        await ctx.send(
            "Fuck off. This doesn't belong in production code! Bother Nichole instead."
        )

    @commands.guild_only()
    @commands.check(check_if_bot_manager)
    @commands.command()
    async def load(self, ctx, ext: str):
        """Loads a cog, bot manager only."""
        try:
            self.bot.load_extension("cogs." + ext)
        except:
            await ctx.send(
                f":x: Cog loading failed, traceback: "
                f"```\n{traceback.format_exc()}\n```"
            )
            return
        self.bot.log.info(f"Loaded ext {ext}")
        await ctx.send(f":white_check_mark: `{ext}` successfully loaded.")

    @commands.guild_only()
    @commands.check(check_if_bot_manager)
    @commands.command()
    async def unload(self, ctx, ext: str):
        """Unloads a cog, bot manager only."""
        self.bot.unload_extension("cogs." + ext)
        self.bot.log.info(f"Unloaded ext {ext}")
        await ctx.send(f":white_check_mark: `{ext}` successfully unloaded.")

    @commands.check(check_if_bot_manager)
    @commands.command()
    async def reload(self, ctx, ext="_"):
        """Reloads a cog, bot manager only."""
        if ext == "_":
            ext = self.lastreload
        else:
            self.lastreload = ext

        try:
            self.bot.unload_extension("cogs." + ext)
            self.bot.load_extension("cogs." + ext)
            await self.cog_load_actions(ext)
        except:
            await ctx.send(
                f":x: Cog reloading failed, traceback: "
                f"```\n{traceback.format_exc()}\n```"
            )
            return
        self.bot.log.info(f"Reloaded ext {ext}")
        await ctx.send(f":white_check_mark: `{ext}` successfully reloaded.")

    @commands.guild_only()
    @commands.check(check_if_bot_manager)
    @commands.command()
    async def speak(self, ctx, channel: discord.TextChannel, *, the_text: str):
        """Repeats a given text in a given channel, staff only."""
        await channel.send(the_text)


def setup(bot):
    bot.add_cog(Admin(bot))
