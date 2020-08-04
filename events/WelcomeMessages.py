from discord.ext.commands import Cog
from discord.utils import get

from utils import db, basic_utilties as utils


class WelcomeMessages(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        # Welcome Messages
        is_guild_in_db = db.field(f"SELECT guild_id FROM guild_welcome WHERE guild_id = {member.guild.id}")
        if is_guild_in_db is None:
            return
        else:
            message = db.field(f"SELECT welcome_message FROM guild_welcome WHERE guild_id = {member.guild.id}")
            channel_id = db.field(f"SELECT welcome_channel_id FROM guild_welcome WHERE guild_id = {member.guild.id}")
            mention = member.mention
            guild = member.guild.name
            welcome_message = utils.embed_message(title="New Member!",
                                                  message=str(message).format(member=member, mention=mention, guild=guild),
                                                  footer_icon=member.guild.icon_url,
                                                  footer_text=f"| {guild}",
                                                  thumbnail=member.avatar_url)
            channel = self.bot.get_channel(id=channel_id)
            await channel.send(embed=welcome_message)
        # Welcome Messages End

def setup(bot):
    bot.add_cog(WelcomeMessages(bot))