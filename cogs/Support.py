from discord.colour import Colour
from discord.ext.commands import Cog
from discord.ext.commands import command

from utils import basic_utilties as utils, db

class Support(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @command(name="suggest", aliases=["suggestion"])
    async def support_suggest(self, ctx, *, suggestion: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if suggestion is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="The correct syntax is:\n" +
                                          f"`{self.prefix}suggest [Suggestion Here]`",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        suggestion_blacklist = db.field(f"SELECT * FROM suggestion_blacklist WHERE member_id = {ctx.author.id}")
        if suggestion_blacklist is not None:
            return await ctx.message.add_reaction("❌")
        suggestion_channel = self.bot.get_channel(id=710978375426244729)
        message = utils.embed_message(title="Suggestion!",
                                      message="```\n" +
                                      suggestion + "\n" +
                                      "```",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=f"Suggestion By -> {ctx.author} / {ctx.author.id} / Server ID -> {ctx.guild.id}")
        await suggestion_channel.send(embed=message)
        await ctx.message.add_reaction("\N{OK HAND SIGN}")

    @command(name="support")
    async def support_server(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title="Support Server Invite",
                                      message="You can join the support server via this link: https://discord.gg/tKZbxAF",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text="Just ping the `Developer` role if you're in need of assistance.")
        await ctx.send(embed=message)

    @command(name="invite")
    async def support_invite_bot(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title="Invite Platform to your server!",
                                      footer_icon=self.bot.user.avatar_url,
                                      url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot")
        await ctx.send(embed=message)

def setup(bot):
    bot.add_cog(Support(bot))