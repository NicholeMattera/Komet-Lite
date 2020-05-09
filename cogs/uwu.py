import discord
from discord.ext import commands
from discord.ext.commands import Cog
import random
import re

class Uwu(Cog):
    """
    UwU (つ✧ω✧)つ
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=["owoify"])
    async def uwuify(self, ctx, *, message: str):
        """Tuwns any text given into uwu wanguage (｡♥‿♥｡)"""

        faces = [
            "(*^ω^)",
            "(◕‿◕✿)",
            "(◕ᴥ◕)",
            "ʕ•ᴥ•ʔ",
            "ʕ￫ᴥ￩ʔ",
            "(*^.^*)",
            "owo",
            "(｡♥‿♥｡)",
            "uwu",
            "(*￣з￣)",
            ">w<",
            "^w^",
            "(つ✧ω✧)つ",
            "(/ =ω=)/",
        ]

        message = re.sub(r"(?:L|R)", "W", message)
        message = re.sub(r"(?:l|r)", "w", message)
        message = re.sub(r"n([aeiou])", r"ny\1", message)
        message = re.sub(r"N([aeiou])", r"Ny\1", message)
        message = re.sub(r"N([AEIOU])", r"NY\1", message)
        message = re.sub("OVE", "UV", message)
        message = re.sub(r"ove", "uv", message, flags=re.I)
        message = re.sub(r"!+", f" {random.choice(faces)} ", message)

        await ctx.message.delete()
        await ctx.send(f"**{ctx.author.name}** {message}")


def setup(bot):
    bot.add_cog(Uwu(bot))
