from discord import Member, Embed
from discord.colour import Colour
from discord.ext.commands import Cog, group, has_permissions, guild_only
from discord.ext.commands import command

from utils import db, basic_utilties as utils

class Prefix(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @group(name="prefix", invoke_without_command=True)
    @guild_only()
    async def prefix_get(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title=f"Bots Prefix",
                                      message=f"The bots current prefix is -> `{self.prefix}`\n" +
                                              f"You can change the bots prefix by doing -> `{self.prefix}prefix set [New Prefix]`",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @prefix_get.command(name="set")
    @has_permissions(manage_guild=True)
    @guild_only()
    async def prefix_set(self, ctx, new_prefix: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if new_prefix is None:
            return await ctx.send("Your new prefix can't be nothing.")
        if len(new_prefix) > 10:
            return await ctx.send("Your new prefix can't be longer than 10 characters.")
        message = utils.embed_message(title=f"Prefix Updated",
                                      message=f"The bots new prefix in this server is -> `{new_prefix}`",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        db.execute(f"UPDATE guild_settings SET prefix = ? WHERE guild_id = ?", new_prefix, ctx.guild.id)
        db.commit()
        await ctx.send(embed=message)

def setup(bot):
    bot.add_cog(Prefix(bot))