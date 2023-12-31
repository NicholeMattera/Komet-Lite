import discord
import config
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_verified


class Links(Cog):
    """
    Commands for easily linking to projects.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.check(check_if_verified)
    @commands.command(hidden=True)
    async def pegaswitch(self, ctx):
        """Link to the Pegaswitch repo"""
        await ctx.send("https://github.com/reswitched/pegaswitch")

    @commands.check(check_if_verified)
    @commands.command(hidden=True, aliases=["atmos", "ams"])
    async def atmosphere(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://github.com/atmosphere-nx/atmosphere")

    @commands.check(check_if_verified)
    @commands.command(hidden=True, aliases=["bootloader"])
    async def hekate(self, ctx):
        """Link to the Hekate repo"""
        await ctx.send("https://github.com/CTCaer/hekate")

    @commands.check(check_if_verified)
    @commands.command(hidden=True, aliases=["xyproblem"])
    async def xy(self, ctx):
        """Link to the "What is the XY problem?" post from SE"""
        await ctx.send(
            "<https://meta.stackexchange.com/q/66377/285481>\n\n"
            "TL;DR: It's asking about your attempted solution "
            "rather than your actual problem.\n"
            "It's perfectly okay to want to learn about a "
            "solution, but please be clear about your intentions "
            "if you're not actually trying to solve a problem."
        )

    @commands.check(check_if_verified)
    @commands.command(hidden=True, aliases=["guides", "link"])
    async def guide(self, ctx):
        """Link to the guide(s)"""

        await ctx.send(
            "**Generic starter guides:**\n"
            "SDSetup Guide: "
            "<https://switch.homebrew.guide>\n"
            "\n"
            "**Specific guides:**\n"
            "Manually Updating/Downgrading (with HOS): "
            "<https://switch.homebrew.guide/usingcfw/manualupgrade>\n"
            "Manually Repairing/Downgrading (without HOS): "
            "<https://switch.homebrew.guide/usingcfw/manualchoiupgrade>\n"
            "How to get started developing Homebrew: "
            "<https://switch.homebrew.guide/homebrew_dev/introduction>"
        )

    @commands.check(check_if_verified)
    @commands.command(hidden=True, aliases=["sdfiles"])
    async def kosmos(self, ctx):
        """Link to the latest Kosmos release"""
        await ctx.send("https://github.com/Team-Neptune/DeepSea/releases/latest")

    @commands.check(check_if_verified)
    @commands.command(hidden=True, aliases=["sd"])
    async def sdsetup(self, ctx):
        """Link to SD Setup"""
        await ctx.send("https://sdsetup.com")

    @commands.check(check_if_verified)
    @commands.command()
    async def source(self, ctx):
        """Gives link to source code."""
        await ctx.send(
            f"You can find my source at {config.source_url}. "
            "Serious PRs and issues welcome!"
        )


def setup(bot):
    bot.add_cog(Links(bot))
