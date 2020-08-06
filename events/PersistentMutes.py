from discord.ext.commands import Cog
from discord.utils import get

from utils import db, basic_utilties as utils


class PersistentMutes(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        # Check if Muted
        is_guild_in_db = db.field(f"SELECT guild_id FROM guild_mutes WHERE guild_id = {member.guild.id}")
        if is_guild_in_db is None:
            return

        check_if_user_muted_in_guild = db.field(f"SELECT user_id FROM guild_mutes WHERE guild_id = ? AND user_id = ?",
                                                member.guild.id, member.id)
        if check_if_user_muted_in_guild is None:
            return

        get_mute_id = db.field(f"SELECT mute_role FROM guild_settings WHERE guild_id = {member.guild.id}")
        get_mute_role = member.guild.get_role(role_id=get_mute_id)
        await member.add_roles(get_mute_role, reason="Mute Role Persist")
        # Check if Muted End

def setup(bot):
    bot.add_cog(PersistentMutes(bot))