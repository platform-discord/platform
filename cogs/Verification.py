from discord import TextChannel
from discord.ext.commands import Cog, group, has_permissions, MissingPermissions

from utils import db, basic_utilties as utils

import asyncio

class Verification(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @group(name="verification", aliases=["verify"], invoke_without_command=True)
    @has_permissions(manage_guild=True)
    async def manage_verification(self, ctx):  # , channel: TextChannel = None, role: str = None
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title="Verification Setup.",
                                      message="Verification Setup Process:\n" +
                                              f"`{self.prefix}verification setup [Text Channel] [Role]` -> Sets up verification in that channel with a given role.\n" +
                                              f"`{self.prefix}verification reset` -> Removes verification from your guild.",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @manage_verification.command(name="setup")
    @has_permissions(manage_guild=True)
    async def manage_verification_setup(self, ctx, channel: TextChannel = None, role: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if channel is None or role is None:
            message = utils.embed_message(title="Verification Setup.",
                                          message="Verification Setup Process:\n" +
                                                  f"`{self.prefix}verification setup #text-channel role-name` -> Sets up verification in that channel with a given role.\n" +
                                                  f"`{self.prefix}verification reset` -> Removes verification from your guild.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        verification_message = utils.embed_message(title="Human Verification",
                                                   message="React to this to verify yourself!",
                                                   footer_icon=ctx.guild.icon_url,
                                                   footer_text="| " + ctx.guild.name)

        # Check if the guild is in the database.
        guild_in_db_already = db.field(f"SELECT guild_id FROM guild_verification WHERE guild_id = ?", ctx.guild.id)
        if guild_in_db_already is not None:
            await ctx.send(
                "Are you sure you would like to update your verification? This will stop your current one from working.")
            try:
                def check(m):
                    return m.author == ctx.author

                wait_for_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} you ran out of time to answer.")
            else:
                user_reply = wait_for_reply.content.lower()
                if not user_reply.startswith("y"):
                    return await ctx.send("Okay, won't be changing anything!")
                elif user_reply.startswith("y"):
                    message = await channel.send(embed=verification_message)
                    await message.add_reaction("\N{OK HAND SIGN}")
                    role = await utils.find_roles(ctx.guild, role)
                    db.execute(
                        f"UPDATE guild_verification SET message_id = ?, role_id = ? WHERE guild_id = ?", message.id, role.id, ctx.guild.id)
                    db.commit()
                    success_message = utils.embed_message(title="Success!",
                                                          message=f"Successfully updated your verification Channel/Role to {channel.mention}/{role.mention}",
                                                          footer_icon=self.bot.user.avatar_url,
                                                          footer_text=utils.random_message())
                    await ctx.send(embed=success_message)
        elif guild_in_db_already is None:
            message = await channel.send(embed=verification_message)
            await message.add_reaction("\N{OK HAND SIGN}")
            role = await utils.find_roles(ctx.guild, role)
            db.execute(f"INSERT INTO guild_verification(guild_id, message_id, role_id) VALUES(?, ?, ?)", ctx.guild.id,
                       message.id, role.id)
            db.commit()
            success_message = utils.embed_message(title="Success!",
                                                  message=f"Successfully set your verification Channel/Role to {channel.mention}/{role.mention}",
                                                  footer_icon=self.bot.user.avatar_url,
                                                  footer_text=utils.random_message())
            await ctx.send(embed=success_message)

    @manage_verification.command(name="reset")
    @has_permissions(manage_guild=True)
    async def manage_verification_reset(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        await ctx.send("Are you sure you'd like to reset this guilds verification? This will stop it from working.")
        try:
            def check(m):
                return m.author == ctx.author

            wait_for_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} you ran out of time to answer.")
        else:
            user_reply = wait_for_reply.content.lower()
            if not user_reply.startswith("y"):
                return await ctx.send("Okay, won't reset your verification.")
            elif user_reply.startswith("y"):
                is_guild_in_db = db.field(f"SELECT * FROM guild_verification WHERE guild_id = ?", ctx.guild.id)
                if is_guild_in_db is None:
                    message = utils.embed_message(title="Error!",
                                                  message="This server is not in the database for verification.",
                                                  footer_icon=self.bot.user.avatar_url,
                                                  footer_text=utils.random_message())
                    return await ctx.send(embed=message)
                success_message = utils.embed_message(title="Success!",
                                                      message=f"Successfully removed verification from the guild.",
                                                      footer_icon=self.bot.user.avatar_url,
                                                      footer_text=utils.random_message())
                db.execute(f"DELETE FROM guild_verification WHERE guild_id = {ctx.guild.id}")
                db.commit()
                await ctx.send(embed=success_message)

def setup(bot):
    bot.add_cog(Verification(bot))
