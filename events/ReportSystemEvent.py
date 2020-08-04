from discord.ext.commands import Cog

from utils import db, basic_utilties as utils

class ReportSystemEvent(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        check_if_id_in_db = db.field(f"SELECT * FROM guild_reports WHERE guild_id = {channel.guild.id}")

        if check_if_id_in_db is None:
            return

        db.execute(f"DELETE FROM guild_reports WHERE guild_id = {channel.guild.id}")
        db.commit()
        utils.log("Removed guild from reports table.")

def setup(bot):
    bot.add_cog(ReportSystemEvent(bot))