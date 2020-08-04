import re
from typing import Optional

from discord import Member
from discord.ext.commands import Cog, group, has_permissions

from utils import basic_utilties as utils

class Purge(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

        # re.search("<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>", m.content)
        # re.search("<(?P<name>[a-zA-Z0-9_]{2,32})>", m.content)

    @group(name="purge", invoke_without_command=True)
    @has_permissions(manage_messages=True)
    async def moderation_purge(self, ctx, member: Optional[Member] = None, amount: int = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if amount is None:
            message = f"""
            `{self.prefix}purge [Amount]` -> Purges a specific amount of messages.
            `{self.prefix}purge match [Word] [Amount]` -> Purges a specific amount of messages containing a specific word.
            `{self.prefix}purge images [Amount]` -> Purges a specific amount of messages that contain images/videos.
            `{self.prefix}purge [User] [Amount]` -> Purges a specific amount of messages sent by a certain user.
            `{self.prefix}purge emojis [Amount]` -> Purges a specific amount of messages that contain emojis.
            *DISCLAIMER: Purging emojis only work with custom emojis so emojis like ♥ will not work.*
            """
            embed = utils.embed_message(title="Purge Command",
                                        message=message,
                                        footer_icon=self.bot.user.avatar_url,
                                        footer_text=utils.random_message())
            await ctx.send(embed=embed)
        if member:
            def check(m):
                return m.author == member
            await ctx.channel.purge(limit=(amount + 1), check=check)
        else:
            await ctx.channel.purge(limit=(amount + 1))

    @moderation_purge.command(name="match")
    @has_permissions(manage_messages=True)
    async def moderation_purge_match(self, ctx, word: str = None, amount: int = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if amount is None or word is None:
            message = f"""
            `{self.prefix}purge [Amount]` -> Purges a specific amount of messages.
            `{self.prefix}purge match [Word] [Amount]` -> Purges a specific amount of messages containing a specific word.
            `{self.prefix}purge images [Amount]` -> Purges a specific amount of messages that contain images/videos.
            `{self.prefix}purge [User] [Amount]` -> Purges a specific amount of messages sent by a certain user.
            `{self.prefix}purge emojis [Amount]` -> Purges a specific amount of messages that contain emojis.
            *DISCLAIMER: Purging emojis only work with custom emojis so emojis like ♥ will not work.*
            """
            embed = utils.embed_message(title="Purge Command",
                                        message=message,
                                        footer_icon=self.bot.user.avatar_url,
                                        footer_text=utils.random_message())
            await ctx.send(embed=embed)
        def check(m):
            return word in m.content

        await ctx.channel.purge(limit=(amount + 1), check=check)

    @moderation_purge.command(name="images")
    @has_permissions(manage_messages=True)
    async def moderation_purge_images(self, ctx, amount: int = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if amount is None:
            message = f"""
            `{self.prefix}purge [Amount]` -> Purges a specific amount of messages.
            `{self.prefix}purge [User] [Amount]` -> Purges a specific amount of messages sent by a certain user.
            `{self.prefix}purge match [Word] [Amount]` -> Purges a specific amount of messages containing a specific word.
            `{self.prefix}purge images [Amount]` -> Purges a specific amount of messages that contain images/videos.
            `{self.prefix}purge emojis [Amount]` -> Purges a specific amount of messages that contain emojis.
            *DISCLAIMER: Purging emojis only work with custom emojis so emojis like ♥ will not work.*
            """
            embed = utils.embed_message(title="Purge Command",
                                        message=message,
                                        footer_icon=self.bot.user.avatar_url,
                                        footer_text=utils.random_message())
            await ctx.send(embed=embed)

        def check(m):
            return m.attachments

        await ctx.channel.purge(limit=(amount + 1), check=check)

    @moderation_purge.command(name="emojis")
    @has_permissions(manage_messages=True)
    async def moderation_purge_emojis(self, ctx, amount: int = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if amount is None:
            message = f"""
            `{self.prefix}purge [Amount]` -> Purges a specific amount of messages.
            `{self.prefix}purge match [Word] [Amount]` -> Purges a specific amount of messages containing a specific word.
            `{self.prefix}purge images [Amount]` -> Purges a specific amount of messages that contain images/videos.
            `{self.prefix}purge [User] [Amount]` -> Purges a specific amount of messages sent by a certain user.
            `{self.prefix}purge emojis [Amount]` -> Purges a specific amount of messages that contain emojis.
            *DISCLAIMER: Purging emojis only work with custom emojis so emojis like ♥ will not work.*
            """
            embed = utils.embed_message(title="Purge Command",
                                        message=message,
                                        footer_icon=self.bot.user.avatar_url,
                                        footer_text=utils.random_message())
            await ctx.send(embed=embed)

        def check(m):
            return re.search("<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>", m.content)

        await ctx.channel.purge(limit=(amount + 1), check=check)

def setup(bot):
    bot.add_cog(Purge(bot))