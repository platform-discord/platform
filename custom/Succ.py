import discord
from discord.ext.commands import Cog, command
from discord.utils import get


class Succ(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = 530497097095446538
        """
        Succ Cog
        """

    @Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == self.id:
            if member.bot:
                await member.kick(reason="No fuckin bots")

def setup(bot):
    bot.add_cog(Succ(bot))
