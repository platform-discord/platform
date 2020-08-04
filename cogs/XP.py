import asyncio
from random import randint

from discord import TextChannel, Member
from discord.ext.commands import Cog, group, has_permissions, command

import time

from utils import db, basic_utilties as utils

class XP(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @Cog.listener()
    async def on_message(self, message):
        author = message.author
        guild = message.guild
        is_guild_enabled = db.field(f"SELECT enabled FROM guild_rank_settings WHERE guild_id = {guild.id}")
        if is_guild_enabled is None or 0: return
        if author.bot: return
        xp_to_add = randint(15, 50)
        xp_lock = int(time.time() + randint(60, 90))
        is_user_in_db = db.record(f"SELECT * FROM guild_ranks WHERE guild_id = {guild.id} AND member_id = {author.id}")

        if is_user_in_db is None:
            db.execute(f"INSERT INTO guild_ranks VALUES({guild.id}, {author.id}, {xp_to_add}, 0, {xp_lock})")
            db.commit()
            return

        current_xp = db.field(f"SELECT xp FROM guild_ranks WHERE guild_id = {guild.id} AND member_id = {author.id}")
        current_level = db.field(f"SELECT level FROM guild_ranks WHERE guild_id = {guild.id} AND member_id = {author.id}")
        new_lvl = int(((current_xp + xp_to_add) // 42) ** 0.55)
        get_member_time_lock = db.field(f"SELECT xp_lock FROM guild_ranks WHERE guild_id = {guild.id} AND member_id = {author.id}")

        if int(time.time()) < get_member_time_lock:
            return

        db.execute(f"UPDATE guild_ranks SET xp = ?, level = ?, xp_lock = ? WHERE guild_id = ? AND member_id = ?",
                   current_xp + xp_to_add, new_lvl, xp_lock, guild.id, author.id)
        db.commit()

        if new_lvl > current_level:
            lvl_up_channel_id = db.field(f"SELECT channel_id FROM guild_rank_settings WHERE guild_id = {guild.id}")
            if lvl_up_channel_id is None: return
            level_up_message = utils.embed_message(title="Level Up!",
                                                   message=f"{author.mention} has just leveled up to level {new_lvl}!",
                                                   footer_icon=self.bot.user.avatar_url,
                                                   footer_text=utils.random_message())
            lvl_up_channel = self.bot.get_channel(id=lvl_up_channel_id)
            await lvl_up_channel.send(embed=level_up_message)

    @command(name="rank")
    async def get_rank(self, ctx, member: Member = None):
        is_guild_enabled = db.field(f"SELECT enabled FROM guild_rank_settings WHERE guild_id = {ctx.guild.id}")
        if is_guild_enabled is None or 0: return
        if member == None:
            member = ctx.author
        current_xp = db.field(f"SELECT xp FROM guild_ranks WHERE guild_id = {ctx.guild.id} AND member_id = {member.id}")
        current_level = db.field(f"SELECT level FROM guild_ranks WHERE guild_id = {ctx.guild.id} AND member_id = {member.id}")
        message = utils.embed_message(title=f"{member}'s Level",
                                      message="**Current XP:**\n" +
                                              f"{current_xp}\n" +
                                              "**Current Level:**\n" +
                                              f"{current_level}",
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message(),
                                              thumbnail=member.avatar_url)
        await ctx.send(embed=message)

    @group(name="xp", invoke_without_command=True)
    @has_permissions(manage_guild=True)
    async def rank_xp(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = f"""
        **To enable XP you must have a channel set up for messages to go to.**
        `{self.prefix}xp channel [Text Channel]` -> Sets the channel for all level up messages to go to, leave this blank to reset it.
        `{self.prefix}xp reset` -> Reset everyone's XP in the server.
        """
        message = utils.embed_message(title="XP Command",
                                      message=message,
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @rank_xp.command(name="channel")
    @has_permissions(manage_guild=True)
    async def rank_xp_set_channel(self, ctx, channel: TextChannel = None):
        if channel is None:
            await ctx.send("Would you like to reset the channel that level up messages go to?")
            try:
                def check(m):
                    return m.author.id == ctx.author.id
                wait_for_user_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send(f"{ctx.author.mention} you ran out of time!")
            else:
                user_reply = wait_for_user_reply.content.lower()
                if not user_reply == "yes":
                    return await ctx.send("Ok, won't reset")
                elif user_reply == "yes":
                    db.execute(f"DELETE FROM guild_rank_settings WHERE guild_id = {ctx.guild.id}")
                    db.commit()
                    return await ctx.send("✔ Successfully reset your level up messages channel")
        is_channel_already_set = db.field(f"SELECT channel_id FROM guild_rank_settings WHERE guild_id = {ctx.guild.id}")
        if is_channel_already_set is not None:
            db.execute(f"UPDATE guild_rank_settings SET channel_id = {channel.id} WHERE guild_id = {ctx.guild.id}")
            db.commit()
            return await ctx.send(f"✔ Successfully updated your level up messages to go to {channel.mention}")
        db.execute(f"INSERT INTO guild_rank_settings(guild_id, channel_id, enabled) VALUES(?, ?, ?)", ctx.guild.id, channel.id, 1)
        db.commit()
        await ctx.send(f"✔ Successfully set your level up messages to go to {channel.mention}")

    @rank_xp.command(name="reset")
    @has_permissions(manage_guild=True)
    async def rank_xp_reset(self, ctx):
        is_guild_enabled = db.field(f"SELECT enabled FROM guild_rank_settings WHERE guild_id = {ctx.guild.id}")
        if is_guild_enabled is None or 0: return
        await ctx.send("Are you sure you want to reset everyone's level?")
        try:
            def check(m):
                return m.author.id == ctx.author.id
            wait_for_user_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author.mention} you ran out of time!")
        else:
            user_reply = wait_for_user_reply.content.lower()
            if not user_reply == "yes":
                return await ctx.send("Ok, won't reset")
            elif user_reply == "yes":
                db.execute(f"DELETE FROM guild_ranks WHERE guild_id = {ctx.guild.id}")
                db.commit()
                return await ctx.send("✔ Successfully reset everyone's xp.")

def setup(bot):
    bot.add_cog(XP(bot))