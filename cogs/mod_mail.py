
import config
import discord
from discord.ext import commands
from discord.ext.commands import Cog


class ModMail(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['creport'])
    async def modmail(self, ctx, *, body: str = ""):
        """Sends a modmail"""
        modmail_channel = self.bot.get_channel(config.modmail_channel)
        embed =  discord.Embed(title=f"New modmail from {ctx.author.name}!",
                               description=f"**Content:** {body}")
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await modmail_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ModMail(bot))
