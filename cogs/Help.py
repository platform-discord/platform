import asyncio

from discord import Member, Embed
from discord.colour import Colour
from discord.ext.commands import Cog
from discord.ext.commands import group
from discord.ext.commands import has_permissions

from utils import basic_utilties as utils


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @group(aliases=["h"], invoke_without_command=True)
    async def help(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Help | 1/2",
                  colour=Colour.blurple())
        e2 = Embed(title="Help | 2/2",
                  colour=Colour.blurple())

        e.add_field(name="⚔  Moderation Help",
                    value=f"{self.prefix}help moderation\n" +
                          "*Alias(es): mod*",
                    inline=False)
        e.add_field(name="👮‍♂️  Management Help",
                    value=f"{self.prefix}help management",
                    inline=False)
        e.add_field(name="🎤  Support Help",
                    value=f"{self.prefix}help support",
                    inline=False)
        e.add_field(name="⚽  Fun Help",
                    value=f"{self.prefix}help fun",
                    inline=False)
        e2.add_field(name="⭐  Premium Help",
                    value=f"{self.prefix}help premium\n" +
                          "*Alias(es): prem*",
                    inline=False)
        e2.add_field(name="🛡  XP Help",
                    value=f"{self.prefix}help xp",
                    inline=False)
        e2.add_field(name="📝  Notes Help",
                     value=f"{self.prefix}help notes",
                     inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())
        e2.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        content = [e, e2]
        cur_page = 1
        pages = 2

        message = await ctx.send(embed=content[cur_page - 1])

        await message.add_reaction("👈")
        await message.add_reaction("👉")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["👈", "👉", "❌"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # Waiting for the reaction to be added and it will timeout after 60 seconds.

                if str(reaction.emoji) == "👉" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "👈" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @help.command(name="moderation", aliases=["mod"])
    async def help_moderation(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Moderation Help | 1/3",
                  colour=Colour.blurple())
        e2 = Embed(title="Moderation Help | 2/3",
                  colour=Colour.blurple())
        e3 = Embed(title="Moderation Help | 3/3",
                   colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}mute",
                    value="Mutes a user for a certain amount of time.",
                    inline=False)
        e.add_field(name=f"{self.prefix}kick",
                    value="Kicks a given user for a given reason.",
                    inline=False)
        e.add_field(name=f"{self.prefix}ban",
                    value="Bans a given user for a given reason.",
                    inline=False)
        e.add_field(name=f"{self.prefix}unmute",
                    value="Unmutes a given user that's muted.",
                    inline=False)

        e2.add_field(name=f"{self.prefix}hackban",
                     value="Bans a user even when they're not in the server",
                     inline=False)
        e2.add_field(name=f"{self.prefix}setnick",
                     value="Sets a new nickname for a given user.",
                     inline=False)
        e2.add_field(name=f"{self.prefix}whois",
                     value="Gives information on the user account.",
                     inline=False)
        e2.add_field(name=f"{self.prefix}members",
                     value="Gives a list of members of a given roles",
                     inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())
        e2.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())
        e3.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        content = [e, e2, e3]
        cur_page = 1
        pages = 3

        message = await ctx.send(embed=content[cur_page - 1])

        await message.add_reaction("👈")
        await message.add_reaction("👉")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["👈", "👉", "❌"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # Waiting for the reaction to be added and it will timeout after 60 seconds.

                if str(reaction.emoji) == "👉" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "👈" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @help.command(name="management")
    async def help_management(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Management Help | 1/2",
                  colour=Colour.blurple())
        e2 = Embed(title="Management Help | 2/2",
                  colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}role",
                    value="Creates or deletes a role or adds or removes\n" +
                          "a role to/from someone.",
                    inline=False)
        e.add_field(name=f"{self.prefix}prefix",
                    value="Gets or sets the prefix of the bot in the server.",
                    inline=False)
        e.add_field(name=f"{self.prefix}welcome",
                    value="Sets up welcome messages for when someone joins.",
                    inline=False)
        e.add_field(name=f"{self.prefix}verification",
                    value="Sets up verification for when people join.",
                    inline=False)
        e2.add_field(name=f"{self.prefix}reports",
                    value="Sets up the reporting system.",
                    inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())
        e2.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        content = [e, e2]
        cur_page = 1
        pages = 2

        message = await ctx.send(embed=content[cur_page - 1])

        await message.add_reaction("👈")
        await message.add_reaction("👉")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["👈", "👉", "❌"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # Waiting for the reaction to be added and it will timeout after 60 seconds.

                if str(reaction.emoji) == "👉" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "👈" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @help.command(name="support")
    async def help_support(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Support Help | 1/1",
                  colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}suggest",
                    value="Suggest a new feature to the bot developer.",
                    inline=False)
        e.add_field(name=f"{self.prefix}support",
                    value="Sends an invite to the support server.",
                    inline=False)
        e.add_field(name=f"{self.prefix}invite",
                    value="Invites the bot to the server.",
                    inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        await ctx.send(embed=e)

    @help.command(name="fun")
    async def help_fun(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Fun Help | 1/4",
                  colour=Colour.blurple())
        e2 = Embed(title="Fun Help | 2/4",
                  colour=Colour.blurple())
        e3 = Embed(title="Fun Help | 3/4",
                   colour=Colour.blurple())
        e4 = Embed(title="Fun Help | 3/4",
                   colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}urban",
                    value="Gives you the definition of any word on urbandictionary",
                    inline=False)
        e.add_field(name=f"{self.prefix}timezone",
                    value="Gets the time in a given timezone\n" +
                          "https://kal-byte.co.uk/timezones.txt for all available timezones",
                    inline=False)
        e.add_field(name=f"{self.prefix}rps",
                    value="Little bit of rock paper scissors with the bot",
                    inline=False)
        e.add_field(name=f"{self.prefix}rng",
                    value="Test your luck with rng with the bot",
                    inline=False)
        e2.add_field(name=f"{self.prefix}babyname",
                    value="Gives you a cute little new name",
                    inline=False)
        e2.add_field(name=f"{self.prefix}poll",
                    value="Generate a poll with the bot",
                    inline=False)
        e2.add_field(name=f"{self.prefix}penis",
                    value="See how big your pp is 😳",
                    inline=False)
        e2.add_field(name=f"{self.prefix}fact",
                    value="Get a random fact",
                    inline=False)
        e3.add_field(name=f"{self.prefix}kanye",
                     value="Gives a random kanye quote",
                     inline=False)
        e3.add_field(name=f"{self.prefix}hug",
                     value="Give someone a hug ♥",
                     inline=False)
        e3.add_field(name=f"{self.prefix}pat",
                     value="Pat someone on the head 😇",
                     inline=False)
        e3.add_field(name=f"{self.prefix}wasted",
                     value="Waste someones pfp",
                     inline=False)
        e4.add_field(name=f"{self.prefix}meme",
                     value="Gives a random meme, probably a normie meme 🤓",
                     inline=False)
        e4.add_field(name=f"{self.prefix}floof",
                     value="Gives a random pic of a cat or dog 🐶🐱",
                     inline=False)
        e4.add_field(name=f"{self.prefix}weather",
                     value="Gives you the weather of a given place 🌧",
                     inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())
        e2.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())
        e3.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        content = [e, e2, e3, e4]
        cur_page = 1
        pages = 4

        message = await ctx.send(embed=content[cur_page - 1])

        await message.add_reaction("👈")
        await message.add_reaction("👉")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["👈", "👉", "❌"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # Waiting for the reaction to be added and it will timeout after 60 seconds.

                if str(reaction.emoji) == "👉" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "👈" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @help.command(name="premium", aliases=["prem"])
    async def help_premium(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Premium Help | 1/1",
                  description="To get premium for your guild, contact kal#1806 on discord.",
                  colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}notable",
                    value="Notable reward system.",
                    inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        await ctx.send(embed=e)

    @help.command(name="xp")
    async def help_xp(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="XP Help | 1/1",
                  colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}xp",
                    value="Gives you options for the XP system.",
                    inline=False)
        e.add_field(name=f"{self.prefix}rank",
                    value="Gets your current xp and rank.",
                    inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        await ctx.send(embed=e)

    @help.command(name="notes")
    async def help_notes(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        e = Embed(title="Notes Help | 1/1",
                  colour=Colour.blurple())

        e.add_field(name=f"{self.prefix}notes",
                    value="Gives you options for the notes system.",
                    inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url, text=utils.random_message())

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Help(bot))
