from discord.ext.commands import Cog
from discord.utils import get

from utils import db


class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Human Verification
        if payload.member.bot:
            return

        if payload.emoji.name != "\N{OK HAND SIGN}":
            return

        get_message_id = db.field("SELECT message_id FROM guild_verification " +
                                  f"WHERE guild_id = {payload.guild_id}")
        if get_message_id is None:
            return

        if get_message_id != payload.message_id:
            return

        member = payload.member
        get_role_id = db.field("SELECT role_id FROM guild_verification " +
                                      f"WHERE guild_id = {payload.guild_id}")
        guild = await self.bot.fetch_guild(guild_id=payload.guild_id)
        verification_role = get(guild.roles, id=get_role_id)
        await member.add_roles(verification_role, reason="Human Verification")
        # Human Verification END

def setup(bot):
    bot.add_cog(Reactions(bot))