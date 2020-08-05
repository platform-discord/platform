import time
from typing import Optional

from discord import TextChannel, Member
from discord.ext.commands import Cog, group, has_permissions, command

from utils import db, basic_utilties as utils

class ReportSystem(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @group(name="reports", invoke_without_command=True)
    @has_permissions(manage_guild=True)
    async def report_system(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title="Report System",
                                      message="**Here you will be able to setup the reporting system.**\n\n" +
                                      f"`{self.prefix}reports set [Text Channel]` -> Sets up the reports system.\n" +
                                      f"`{self.prefix}reports reset` -> Resets the report system.\n" +
                                      f"`{self.prefix}report (Option: User) [Reason]` -> Sends a report to the given reports channel.",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @report_system.command(name="set")
    @has_permissions(manage_guild=True)
    async def report_system_setup(self, ctx, channel: TextChannel):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        check_if_in_db = db.field(f"SELECT * FROM guild_reports WHERE guild_id = ?", ctx.guild.id)

        if check_if_in_db is not None:
            db.execute(f"UPDATE guild_reports SET channel_id = ? WHERE guild_id = ?", channel.id, ctx.guild.id)
            db.commit()
            utils.log(f"Updated a guild in the reports table.")
            return await ctx.send(f"✅ {channel.mention} is now your channel for reports to go to.")

        db.execute(f"INSERT INTO guild_reports(guild_id, channel_id) VALUES(?, ?)", ctx.guild.id, channel.id)
        db.commit()
        utils.log(f"Added new guild to the reports table.")
        return await ctx.send(f"✅ {channel.mention} is now your channel for reports to go to.")

    @report_system.command(name="reset")
    @has_permissions(manage_guild=True)
    async def report_system_reset(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        check_if_in_db = db.field(f"SELECT * FROM guild_reports WHERE guild_id = ?", ctx.guild.id)
        if check_if_in_db is None:
            return await ctx.send("❌ You do not have a reports channel set for this guild")
        db.execute(f"DELETE FROM guild_reports WHERE guild_id = ?", ctx.guild.id)
        db.commit()
        utils.log("Removed guild from the reports table.")
        return await ctx.send("✅ Successfully reset the set reports channel.")

    @command(name="report")
    async def reports_system_report(self, ctx, member: Optional[Member], reason: str):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        get_reports_channel = db.field(f"SELECT channel_id FROM guild_reports WHERE guild_id = ?", ctx.guild.id)
        if get_reports_channel is None:
            return await ctx.send("❌ There is no reports channel set in this guild.\n" +
                                  f"Get the administrator to run `{self.prefix}reports setup`.", delete_after=4)
        channel = ctx.bot.get_channel(id=get_reports_channel)
        await channel.send(f"\N{CROSSED SWORDS} **{ctx.author} reported {member} @ {time.ctime(time.time())}:**\n" +
                           f"*{reason}*")

def setup(bot):
    bot.add_cog(ReportSystem(bot))