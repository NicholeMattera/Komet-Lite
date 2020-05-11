import asyncio
import config
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff
import io
import os
import random
import re


class ListsVerification(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification = ""
        if os.path.exists("data/verification.txt"):
            with open("data/verification.txt", "r") as f:
                self.verification = f.read()

        bot.loop.create_task(self.daily())

    def generate_verification_phrase(self):
        random_words = [
            "colony",
            "carriage",
            "be",
            "employee",
            "empirical",
            "flourish",
            "moral",
            "troop",
            "waterfall",
            "reduction",
            "fraction",
            "goalkeeper",
            "conscious",
            "acceptable",
            "advertising",
            "visual",
            "spin",
            "margin",
            "greeting",
            "continuation",
            "sandwich",
            "upset",
            "stake",
            "safe",
            "rally",
            "reservoir",
            "effort",
            "integration",
            "extent",
            "expression",
            "echo",
            "prove",
            "precedent",
            "inhibition",
            "expect",
            "theft",
            "distinct",
            "part",
            "revolution",
            "player",
            "fragrant",
            "waste",
            "value",
            "profession",
            "quote",
            "room",
            "master",
            "utter",
            "aloof",
            "quantity",
        ]

        self.verification = (
            random.choice(random_words)
            + "_"
            + random.choice(random_words)
            + "_"
            + random.choice(random_words)
        )
        with open("data/verification.txt", "w") as f:
            f.write(self.verification)

    async def reset_verification_channel(self, rules_channel, verification_channel):
        self.generate_verification_phrase()

        # Get all the rules from the rules channel.
        rules_messages = []
        number_of_rules = 0
        async for message in rules_channel.history(limit=None, oldest_first=True):
            if len(message.content.strip()) != 0:
                number_of_rules += 1

            rules_messages.append(message)

        if number_of_rules == 0:
            return

        # Randomly choose which rule to inject the hidden message in.
        random_rule = 0
        if number_of_rules != 1:
            if number_of_rules < 2:
                random_rule = random.randint(0, number_of_rules - 1)
            else:
                # Don't include the first or last rule.
                random_rule = random.randint(1, number_of_rules - 2)

        # Delete all messages from the welcome channel.
        await verification_channel.purge(limit=None)

        # Put all rules in the welcome channel.
        i = 0
        for message in rules_messages:
            content = message.content

            if content.strip():
                i += 1

            if i == random_rule:
                # Find all of the sentences in the random rule.
                matches = list(re.finditer(r"[.|!|?][\W]*\s*", content))

                # Randomly choose where to put the random message in our random rule.
                random_sentence = 0
                if len(matches) != 1:
                    random_sentence = random.randint(0, len(matches) - 1)

                # Insert our verification text.
                pos = matches[random_sentence].end()
                content = (
                    content[:pos]
                    + f' When you have finished reading all of the rules, send a message in this channel that includes "{self.verification}", and the bot will automatically grant you access to the other channels. '
                    + content[pos:]
                )

            message_file = None
            if len(message.attachments) != 0:
                # Lists will only reupload a single image per message.
                attachment = next(
                    (
                        a
                        for a in message.attachments
                        if os.path.splitext(a.filename)[1] in [".png", ".jpg", ".jpeg"]
                    ),
                    None,
                )
                if attachment is not None:
                    message_file = discord.File(
                        io.BytesIO(await attachment.read()),
                        filename=attachment.filename,
                    )

            await verification_channel.send(content=content, file=message_file)

    # Commands

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def reset(self, ctx):
        """Resets the verification channel with the latest rules"""

        rules_channel_id = getattr(config, "rules_channel", 0)
        verification_channel_id = getattr(config, "verification_channel", 0)

        rules_channel = None
        if rules_channel_id != 0:
            rules_channel = self.bot.get_channel(rules_channel_id)

        verification_channel = None
        if verification_channel_id != 0:
            verification_channel = self.bot.get_channel(verification_channel_id)

        if rules_channel is not None and verification_channel is not None:
            await self.reset_verification_channel(rules_channel, verification_channel)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def verifyall(self, ctx):
        """Gives everyone the verification role"""
        verified_role = ctx.guild.get_role(config.verified_role)

        for member in ctx.guild.members:
            if verified_role not in member.roles:
                await member.add_roles(verified_role)

        await ctx.send("All members verified.")

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def verifiedcount(self, ctx):
        """Prints the number of verified members"""
        verified_role = ctx.guild.get_role(config.verified_role)
        await ctx.send(
            f"{ctx.guild.name} has " f"{len(verified_role.members)} verified members!"
        )

    # Listeners

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()

        if not hasattr(config, "verification_channel"):
            return

        # We only care about messages in Rules, and Support FAQ
        if message.channel.id != config.verification_channel:
            return

        # We don't care about messages from bots.
        if message.author.bot:
            return

        await message.delete()

        # We only care if the message contained the verification phrase.
        if self.verification not in message.content:
            return

        # Grant user the verified role.
        verified_role = message.guild.get_role(config.verified_role)
        await message.author.add_roles(verified_role)

    # Tasks

    async def daily(self):
        await self.bot.wait_until_ready()

        if (
            not hasattr(config, "log_channel")
            or not hasattr(config, "rules_channel")
            or not hasattr(config, "verification_channel")
        ):
            return

        log_channel_id = getattr(config, "log_channel", 0)
        rules_channel_id = getattr(config, "rules_channel", 0)
        verification_channel_id = getattr(config, "verification_channel", 0)

        log_channel = self.bot.get_channel(config.log_channel)
        rules_channel = self.bot.get_channel(config.rules_channel)
        verification_channel = self.bot.get_channel(config.verification_channel)

        # Make sure the bot is open.
        while not self.bot.is_closed():
            # Reset the verification channel
            try:
                await self.reset_verification_channel(
                    rules_channel, verification_channel
                )
            except:
                await log_channel.send(
                    "Verification reset has errored: ```" f"{traceback.format_exc()}```"
                )

            # Wait 1 day
            await asyncio.sleep(86400)


def setup(bot):
    bot.add_cog(ListsVerification(bot))
