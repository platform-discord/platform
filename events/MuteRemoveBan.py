from discord.ext.commands import Cog
from discord.utils import get

from utils import db, basic_utilties as utils


class MuteRemoveBan(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_ban(self, guild, member):
        # Check if Muted
        is_guild_in_db = db.field(f"SELECT guild_id FROM guild_mutes WHERE guild_id = {guild.id}")
        if is_guild_in_db is None:
            return

        check_if_user_muted_in_guild = db.field(f"SELECT user_id FROM guild_mutes WHERE guild_id = {guild.id}")
        if check_if_user_muted_in_guild is None:
            return

        db.execute(f"DELETE FROM guild_mutes WHERE guild_id = {guild.id} AND user_id = {member.id}")
        # Check if Muted End

def setup(bot):
    bot.add_cog(MuteRemoveBan(bot))