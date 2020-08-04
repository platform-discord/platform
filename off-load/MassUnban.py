import discord
from discord.ext import commands

class MassUnban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def massunban(self, ctx):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            await ctx.guild.unban(user)
        await ctx.send("Everyone unbanned.")

def setup(bot):
    bot.add_cog(MassUnban(bot))
