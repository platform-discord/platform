from discord.ext.commands import Cog
from discord.utils import get

from utils import db, basic_utilties as utils


class NotableLeave(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_remove(self, member):
        # Notable Members
        guild_id = db.field(f"SELECT guild_id FROM guild_notable_members WHERE guild_id = {member.guild.id}")
        if guild_id is None: return
        is_user_in_db = db.field(f"SELECT member_id FROM guild_notable_members WHERE guild_id = {member.guild.id} AND member_id = {member.id}")
        if is_user_in_db is None: return
        db.execute(f"DELETE FROM guild_notable_members WHERE guild_id = {member.guild.id} AND member_id = {member.id}")
        db.commit()
        # Notable Members End

def setup(bot):
    bot.add_cog(NotableLeave(bot))