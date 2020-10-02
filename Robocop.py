import sys
import logging
import logging.handlers
import traceback
import config
import discord
from discord.ext import commands

stdout_handler = logging.StreamHandler(sys.stdout)

log_format = logging.Formatter(
    "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
)
stdout_handler.setFormatter(log_format)

log = logging.getLogger("discord")
log.setLevel(logging.INFO)
log.addHandler(stdout_handler)


def get_prefix(bot, message):
    prefixes = config.prefixes

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = [
    "cogs.common",
    "cogs.admin",
    "cogs.basic",
    "cogs.links",
    "cogs.lists",
    "cogs.meme",
    "cogs.uwu",
]

intents = discord.Intents.default()
intents.typing = False
intents.members = True

bot = commands.Bot(
    command_prefix=get_prefix,
    pm_help=True,
    description=config.bot_description,
    intents=intents,
)

bot.log = log

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            log.error(f"Failed to load extension {extension}.")
            log.error(traceback.print_exc())


@bot.event
async def on_ready():
    bot.botlog_channel = bot.get_channel(config.botlog_channel)

    log.info(
        f"\nLogged in as: {bot.user.name} - "
        f"{bot.user.id}\ndpy version: {discord.__version__}\n"
    )
    game_name = f"{config.prefixes[0]}help"

    msg = f"{bot.user.name} has started! "
    await bot.botlog_channel.send(msg)

    activity = discord.Activity(name=game_name, type=discord.ActivityType.listening)

    await bot.change_presence(activity=activity)


@bot.event
async def on_error(event_method, *args, **kwargs):
    log.error(f"Error on {event_method}: {sys.exc_info()}")


@bot.event
async def on_command_error(ctx, error):
    error_text = str(error)

    err_msg = (
        f'Error with "{ctx.message.content}" from '
        f"{ctx.message.author} ({ctx.message.author.id}) "
        f"of type {type(error)}: {error_text}"
    )

    log.error(err_msg)

    if not isinstance(error, commands.CommandNotFound):
        err_msg = bot.escape_message(err_msg)
        await bot.botlog_channel.send(err_msg)

    if isinstance(error, commands.NoPrivateMessage):
        return await ctx.send("This command doesn't work on DMs.")
    elif isinstance(error, commands.MissingPermissions):
        roles_needed = "\n- ".join(error.missing_perms)
        return await ctx.send(
            f"{ctx.author.mention}: You don't have the right"
            " permissions to run this command. You need: "
            f"```- {roles_needed}```"
        )
    elif isinstance(error, commands.BotMissingPermissions):
        roles_needed = "\n-".join(error.missing_perms)
        return await ctx.send(
            f"{ctx.author.mention}: Bot doesn't have "
            "the right permissions to run this command. "
            "Please add the following roles: "
            f"```- {roles_needed}```"
        )
    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(
            f"{ctx.author.mention}: You're being "
            "ratelimited. Try in "
            f"{error.retry_after:.1f} seconds."
        )
    elif isinstance(error, commands.CheckFailure):
        return await ctx.send(
            f"{ctx.author.mention}: Check failed. "
            "You might not have the right permissions "
            "to run this command, or you may not be able "
            "to run this command in the current channel."
        )
    elif isinstance(error, commands.CommandInvokeError) and (
        "Cannot send messages to this user" in error_text
    ):
        return await ctx.send(
            f"{ctx.author.mention}: I can't DM you.\n"
            "You might have me blocked or have DMs "
            f"blocked globally or for {ctx.guild.name}.\n"
            "Please resolve that, then "
            "run the command again."
        )
    elif isinstance(error, commands.CommandNotFound):
        # Nothing to do when command is not found.
        return

    help_text = (
        f"Usage of this command is: ```{ctx.prefix}"
        f"{ctx.command.signature}```\nPlease see `{ctx.prefix}help "
        f"{ctx.command.name}` for more info about this command."
    )
    if isinstance(error, commands.BadArgument):
        return await ctx.send(
            f"{ctx.author.mention}: You gave incorrect " f"arguments. {help_text}"
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(
            f"{ctx.author.mention}: You gave incomplete " f"arguments. {help_text}"
        )


bot.run(config.token, bot=True, reconnect=True)
