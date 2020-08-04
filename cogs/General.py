from aiohttp import request
from discord import Member, Embed
from discord.colour import Colour
from discord.ext.commands import Cog
from discord.ext.commands import command

from random import randint

from utils import basic_utilties as utils

class General(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @command(name="avatar", aliases=["av"])
    async def general_avatar(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            member = ctx.author

        e = Embed(title=f"{member.display_name}'s Avatar",
                  colour=Colour.blurple())
        e.set_footer(text=utils.random_message(), icon_url=self.bot.user.avatar_url)
        e.set_image(url=member.avatar_url_as(static_format="png", size=1024))
        await ctx.send(embed=e)

    @command(name="ping", aliases=["latency"])
    async def general_latency(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title=f"{self.bot.user.name}'s latency -> `{int(self.bot.latency * 1000)} ms`")
        await ctx.send(embed=message)

    @command(name="rcolour", aliases=["rcolor"])
    async def general_random_colour(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)

        random_red, random_green, random_blue = randint(0, 255), randint(0, 255), randint(0, 255)
        random_colour = (random_red, random_green, random_blue)
        random_hex = '#%02x%02x%02x' % random_colour
        image = f"https://some-random-api.ml/canvas/colorviewer?hex={random_hex[1:]}"
        message = utils.embed_message(title="Random Colour",
                                      message=f"Hex -> {random_hex}\n" +
                                              f"RGB -> {random_colour}",
                                      colour=Colour.from_rgb(random_red, random_green, random_blue),
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message(),
                                      thumbnail=image)
        await ctx.send(embed=message)

    @command(name="colour", aliases=["color"])
    async def general_colour(self, ctx, colour: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if colour is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}colour [Hex Colour]` -> Generates an Embed with a given colour",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)
        if "#" in colour:
            colour = colour[1:]
        if len(colour) > 6 or len(colour) < 6:
            return await ctx.send("Please enter a 6 digit hex code.")
        image = f"https://some-random-api.ml/canvas/colorviewer?hex={colour}"
        colour_rgb = utils.hex_to_rgb(colour)
        message = utils.embed_message(title="Generated Colour",
                                      message=f"Hex -> {colour}\n" +
                                              f"RGB -> {colour_rgb}",
                                      colour=Colour.from_rgb(colour_rgb[0], colour_rgb[1], colour_rgb[2]),
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message(),
                                      thumbnail=image)
        await ctx.send(embed=message)


def setup(bot):
    bot.add_cog(General(bot))