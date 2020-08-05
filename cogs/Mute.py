import asyncio
import time

from discord import Member
from discord.colour import Colour
from discord.ext import tasks
from discord.ext.commands import Cog, has_permissions, MissingPermissions, command
from discord.ext.commands import group
from discord.utils import get

from utils import db, basic_utilties as utils


class Mute(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""
        self.check_mutes.start()

    @tasks.loop(seconds=1)
    async def check_mutes(self):
        await self.bot.wait_until_ready()
        mutes = db.records(f"SELECT * FROM guild_mutes")
        for record in mutes:
            ends_at = record[2]
            ends_in = int(ends_at - time.time())
            guild = self.bot.get_guild(record[0])
            member = guild.get_member(record[1])
            mute_role_id = db.field(f"SELECT mute_role FROM guild_settings WHERE guild_id = {guild.id}")
            if ends_in < 0:
                db.execute(f"DELETE FROM guild_mutes WHERE user_id = {member.id} AND guild_id = {guild.id}")
                db.commit()
                await member.remove_roles(guild.get_role(mute_role_id))
            else:
                pass

    @command(name="vmute")
    @has_permissions(manage_messages=True)
    async def moderation_voice_chat(self, ctx, user: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if user is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="**Voice Mute Command:**\n" +
                                                  f"`{self.prefix}vmute [User]` -> Voice mutes someone.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)
        check_staff = await utils.is_target_staff(ctx, user)

        if check_staff:
            message = utils.embed_message(message="❌ That user is a staff member",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        muted_message = utils.embed_message(title="User Voice Muted.",
                                            message=f"{ctx.author.mention} has voice muted {user.mention}",
                                            footer_icon=self.bot.user.avatar_url,
                                            footer_text=utils.random_message())

        unmuted_message = utils.embed_message(title="User Voice Unmuted.",
                                              message=f"{ctx.author.mention} has voice unmuted {user.mention}",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())

        if user.voice.mute:
            await user.edit(mute=False, reason=f"Responsible User -> {ctx.author}")
            await ctx.send(embed=muted_message)
        elif not user.voice.mute:
            await user.edit(mute=True, reason=f"Responsible User -> {ctx.author}")
            await ctx.send(embed=unmuted_message)

    @command(name="moderations")
    @has_permissions(manage_messages=True)
    async def moderation_check_mutes(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        moderations = ""
        mutes = db.records(f"SELECT * FROM guild_mutes")
        for record in mutes:
            ends_at = record[2]
            ends_in = int(ends_at - time.time())
            member = ctx.guild.get_member(record[1])
            if member == type(None):
                moderations += f"\n❌ Invalid User -> {ends_in} seconds"
            else:
                moderations += f"\n❌ {member} -> {ends_in} seconds"

        if moderations == "":
            moderations = "No active moderations."

        message = utils.embed_message(title="Active Moderations",
                                      message=moderations,
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @group(name="mute", invoke_without_command=True)
    @has_permissions(manage_messages=True)
    async def moderation_mute(self, ctx, member: Member = None, mute_time: str = None, *, reason: str = "None"):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)

        if member is None or mute_time is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="**Mute Command:**\n" +
                                                  f"`{self.prefix}mute [User] [Time [e.g. 1s, 1m, 1h]] (reason)` -> Mutes a user for a given time and reason.\n" +
                                                  f"`{self.prefix}mute setup [Role Name]` -> Sets the mute role, this will disable the permission to talk in all channels for this role.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        is_muted_role_setup = db.field(f"SELECT mute_role FROM guild_settings WHERE guild_id = {ctx.guild.id}")
        if is_muted_role_setup is None:
            message = utils.embed_message(title="You need to setup your Muted role.",
                                          message=f"Do this by running -> `{self.prefix}mute setup [Role Name]`",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        check_staff = await utils.is_target_staff(ctx, member)
        if check_staff:
            message = utils.embed_message(message="❌ That user is a staff member",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        is_user_muted = db.field(f"SELECT * FROM guild_mutes WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
        if is_user_muted is not None:
            message = utils.embed_message(title="Error.",
                                          message="That user is already muted, if you'd like to update their mute please unmute and remute",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        success_message = utils.embed_message(title="User Muted.",
                                              message=f"{ctx.author.mention} has muted {member.mention} for: {reason} | {mute_time}",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())

        guild_mute_role = get(ctx.guild.roles, id=is_muted_role_setup)
        raw_time = int(mute_time[:-1])
        # Note to self ->
        #                If the guild id is a PK then it will not allow any more from that guild.
        if mute_time.endswith("s"):
            db.execute(f"INSERT INTO guild_mutes(guild_id, user_id, unix_time) VALUES(?, ?, ?)", ctx.guild.id,
                       member.id, int(time.time() + raw_time))
        elif mute_time.endswith("m"):
            db.execute(f"INSERT INTO guild_mutes(guild_id, user_id, unix_time) VALUES(?, ?, ?)", ctx.guild.id,
                       member.id, int(time.time() + (raw_time * 60)))
        elif mute_time.endswith("h"):
            db.execute(f"INSERT INTO guild_mutes(guild_id, user_id, unix_time) VALUES(?, ?, ?)", ctx.guild.id,
                       member.id, int(time.time() + ((raw_time * 60) * 60)))
        else:
            return await ctx.send("Invalid Time")
        db.commit()
        await member.add_roles(guild_mute_role, reason=f"Muted by -> {ctx.author} | Reason -> {reason}")
        await ctx.send(embed=success_message)

    @command(name="unmute")
    @has_permissions(manage_messages=True)
    async def moderation_unmute(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="You must include a user who is muted to unmute.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        success_message = utils.embed_message(title="User Unmuted",
                                              message=f"✔ Successfully unmuted {member.mention}.",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=f"Unmuted by: {ctx.author}")

        get_user_muted_field = db.record(
            f"SELECT * FROM guild_mutes WHERE user_id = ? AND guild_id = ?", member.id, ctx.guild.id)
        if get_user_muted_field is None:
            mute_role_id = db.field(f"SELECT mute_role FROM guild_settings WHERE guild_id = ?", ctx.guild.id)
            if mute_role_id is None:
                message = utils.embed_message(message="❌ You do not have a mute role setup in this guild.",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                return await ctx.send(embed=message)
            mute_role = ctx.guild.get_role(mute_role_id)
            if mute_role in member.roles:
                await member.remove_roles(mute_role, reason=f"Unmuted by -> {ctx.author}")
                await ctx.send(embed=success_message)
            else:
                message = utils.embed_message(message="❌ That user is not muted.",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                return await ctx.send(embed=message)
        elif get_user_muted_field is not None:
            mute_role_id = db.field(f"SELECT mute_role FROM guild_settings WHERE guild_id = ?", ctx.guild.id)
            mute_role = ctx.guild.get_role(mute_role_id)
            db.execute(F"DELETE FROM guild_mutes WHERE guild_id = ? AND user_id = ?", ctx.guild.id, member.id)
            db.commit()
            await member.remove_roles(mute_role, reason=f"Unmuted by -> {ctx.author}")
            await ctx.send(embed=success_message)

    @moderation_mute.command(name="setup")
    @has_permissions(manage_guild=True)
    async def moderation_mute_setup(self, ctx, role: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if role is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="You must include a role to set to your muted role.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        def check(m):
            return m.author == ctx.author

        role = await utils.find_roles(ctx.guild, role)
        is_muted_role_setup = db.field(f"SELECT mute_role FROM guild_settings WHERE guild_id = {ctx.guild.id}")
        count = 0
        if is_muted_role_setup is None:
            await ctx.send(
                "Are you sure you would like to make this your muted role? This will remove the permission for this role to speak in all text channels.")
            try:
                wait_for_user_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} you ran out of time to answer!")
            else:
                reply = wait_for_user_reply.content.lower()
                if not reply.startswith("y"):
                    return await ctx.send("Won't be setting any roles!")
                elif reply.startswith("y"):
                    await ctx.send("Setting permissions for that role now.")
                    db.execute(f"UPDATE guild_settings SET mute_role = ? WHERE guild_id = ?", role.id, ctx.guild.id)
                    db.commit()
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(role, send_messages=False)
                        count += 1
                    success_message = utils.embed_message(title="Success!",
                                                          message=f"Successfully set {role.mention} to your Muted role and set it's permissions in {count} channel(s).",
                                                          footer_icon=self.bot.user.avatar_url,
                                                          footer_text=utils.random_message())
                    await ctx.send(embed=success_message)
        if is_muted_role_setup is not None:
            await ctx.send(
                "Are you sure you would like to update this to your muted role? This will remove the permission for this role to speak in all text channels.")
            try:
                wait_for_user_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} you ran out of time to answer!")
            else:
                reply = wait_for_user_reply.content.lower()
                if not reply.startswith("y"):
                    return await ctx.send("Won't be setting any roles!")
                elif reply.startswith("y"):
                    await ctx.send("Setting permissions for that role now.")
                    db.execute(f"UPDATE guild_settings SET mute_role = ? WHERE guild_id = ?", role.id, ctx.guild.id)
                    db.commit()
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(role, send_messages=False)
                        count += 1
                    success_message = utils.embed_message(title="Success!",
                                                          message=f"Successfully updated {role.mention} to your Muted role and set it's permissions in {count} channel(s).",
                                                          footer_icon=self.bot.user.avatar_url,
                                                          footer_text=utils.random_message())
                    await ctx.send(embed=success_message)

def setup(bot):
    bot.add_cog(Mute(bot))
