
from discord.ext.commands import Cog
from discord.utils import get

from utils import db


class Nickbans(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_update(self, before, after):
        # Nickbans
        check_guild_in_db = db.field(f"SELECT guild_id FROM guild_nick_bans WHERE guild_id = {after.guild.id}")
        check_if_user_is_nick_banned = db.field(f"SELECT member_id FROM guild_nick_bans WHERE guild_id = {after.guild.id} AND member_id = {after.id}")

        if check_guild_in_db is None:
            return

        if check_if_user_is_nick_banned is None:
            return

        if after.display_name != "Nickname Violation":
            await after.edit(nick="Nickname Violation", reason="User is nickbanned")

def setup(bot):
    bot.add_cog(Nickbans(bot))