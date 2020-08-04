import asyncio

import discord
from discord import Member, Object
from discord.colour import Colour
from discord.ext.commands import Cog, MissingPermissions
from discord.ext.commands import command
from discord.ext.commands import has_permissions

from utils import basic_utilties as utils


async def get_user_banned(guild, name_arg):
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if name_arg.lower().startswith(user.name.lower()):
            member_to_unban = Object(id=user.id)
            return member_to_unban
    return None

class Ban(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @command(name="massunban", aliases=["unbanall"])
    @has_permissions(manage_guild=True)
    async def moderation_mass_unban(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        def check(m):
            return m.author == ctx.author
        await ctx.send("Are you sure you want to mass unban? Y/N (10 seconds to answer)")
        try:
            user_input = await self.bot.wait_for("message", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author.mention} you ran out of time to answer.")
        else:
            user_reply = user_input.content.lower()
            if not user_reply.startswith("y"):
                return await ctx.send("Ok, backing out.")
            elif user_reply.startswith("y"):
                await ctx.send("Unbanning all banned users, this may take a while.")
                bans = await ctx.guild.bans()
                for ban in bans:
                    user = ban.user
                    await ctx.guild.unban(user, reason=f"Mass Unban | Responsible User -> {ctx.author}")
                await ctx.send("Successfully unbanned all banned users.")

    @command(name="hackban")
    @has_permissions(ban_members=True)
    async def moderation_hackban(self, ctx, user_id: int = None, *, reason: str = "None"):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if user_id is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}hackban [User ID] (Reason)` -> Bans a user by id, can be given a reason.",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        user_object = Object(id=user_id)
        message = utils.embed_message(title="Member Banned",
                                      message=f"Successfully banned the ID: `{user_id}`",
                                      footer_text=utils.random_message(),
                                      footer_icon=self.bot.user.avatar_url)
        try:
            await ctx.guild.ban(user_object, reason=f"{reason} | Banned By -> {ctx.author}")
        except discord.Forbidden:
            return await ctx.send("I was unable to ban that ID?")
        except discord.NotFound:
            return await ctx.send("I could not ban that ID for some reason...")
        await ctx.send(embed=message)

    @command(name="ban", aliases=["barn", "banish"])
    @has_permissions(ban_members=True)
    async def moderation_ban(self, ctx, member: Member = None, *reason: str):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}ban [User] (Reason)` -> Bans a user, can be given a reason.\n" +
                                                  f"`{self.prefix}unban [User]` -> Unbans a given member.\n",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        target_staff = await utils.is_target_staff(ctx, member)
        if target_staff:
            message = utils.embed_message(message="❌ That user is a staff member",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)
        if len(reason) == 0:
            ban_reason = "None"
        else:
            ban_reason = " ".join(reason)
        message = utils.embed_message(title="Member Banned",
                                      message=f"Successfully banned {member} for: {ban_reason}",
                                      footer_text=f"Their User ID: {member.id}",
                                      footer_icon=self.bot.user.avatar_url)
        try:
            await member.ban(reason=f"{ban_reason} | {ctx.author}")
        except discord.Forbidden:
            return await ctx.send("I was unable to ban that person... :thinking:")
        except discord.NotFound:
            return await ctx.send("I couldn't find that user? :thinking:")
        await ctx.send(embed=message)

    @command(name="unban", aliases=["unbarn", "unbanish"])
    @has_permissions(ban_members=True)
    async def moderation_unban(self, ctx, member: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}ban [User] (Reason)` -> Bans a user, can be given a reason..\n" +
                                                  f"`{self.prefix}unban [User]` -> Unbans a given member.\n",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        member_to_unban = await get_user_banned(ctx.guild, member)
        message = utils.embed_message(title="Member Unbanned",
                                      message=f"Successfully unbanned: {member}",
                                      colour=Colour.red(),
                                      footer_icon=self.bot.user.avatar_url)
        try:
            await ctx.guild.unban(member_to_unban, reason=f"Responsible User: {ctx.author}")
        except discord.Forbidden:
            return await ctx.send("I was unable to unban them for some reason.")
        except discord.NotFound:
            return await ctx.send("I was unable to find them...")
        await ctx.send(embed=message)

def setup(bot):
    bot.add_cog(Ban(bot))