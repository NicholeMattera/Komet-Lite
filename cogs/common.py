from discord.ext.commands import Cog


class Common(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.escape_message = self.escape_message

    def escape_message(self, text: str):
        """Escapes unfun stuff from messages"""
        return str(text).replace("@", "@ ").replace("<#", "# ")


def setup(bot):
    bot.add_cog(Common(bot))
