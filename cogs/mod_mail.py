import config
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.userlogs import get_userlog, userlog
import time


class ModMail(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["creport"])
    async def modmail(self, ctx, *, body: str = ""):
        """Sends a modmail"""

        # Prevent sending of blank messages.
        if len(body.strip()) == 0:
            await ctx.send("A message can not be empty.")
            return

        logs = get_userlog()
        uid = str(ctx.author.id)

        # Get the timeout from the config and default it to 15 seconds.
        timeout = getattr(config, "modmail_timeout", 15)

        # Make sure our user exists in the userlog, and they've sent a message before.
        if uid in logs and "mail" in logs[uid] and len(logs[uid]["mail"]) != 0:
            last_message = logs[uid]["mail"][-1]

            # Prevents sending the same message.
            if last_message["body"].strip() == body.strip():
                await ctx.send("Unable to send message.")
                return

            # Rate limit messages.
            delta_time = int(time.time()) - last_message["timestamp"]
            if delta_time < timeout:
                await ctx.send(
                    f"Please wait {timeout - delta_time} seconds before sending another message."
                )
                return

        # Log messages to the userlog.
        userlog(uid, None, body, "mail", ctx.author.name)

        modmail_channel = self.bot.get_channel(config.modmail_channel)
        embed = discord.Embed(
            title=f"New modmail from {ctx.author.name}!",
            description=f"**Content:** {body}",
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await modmail_channel.send(embed=embed)
        await ctx.send("Message sent.")


def setup(bot):
    bot.add_cog(ModMail(bot))
