from discord import Member, Embed, Forbidden
from discord.colour import Colour
from discord.ext.commands import Cog, group, has_permissions, MissingPermissions
from discord.ext.commands import command

from utils import db, basic_utilties as utils

class BasicModeration(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""

    @command(name="clean")
    @has_permissions(manage_messages=True)
    async def moderation_clean_bots(self, ctx):
        await ctx.message.delete()
        def check(m):
            return m.author.bot
        await ctx.channel.purge(limit=100, check=check)

    @command(name="members")
    @has_permissions(manage_messages=True)
    async def moderation_role_members(self, ctx, *, role: str = None):
        if role is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}members [Role Name]` -> Gives a list of members in a specific role.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)
        in_role = []
        role = await utils.find_roles(ctx.guild, role)
        for member in role.members:
            in_role.append(f"{member.mention}")
        column_1 = in_role
        column_2 = "​"
        if len(in_role) > 1:
            column_1, column_2 = utils.split_list(in_role)
        message = utils.embed_message(title=f"Members of {role.name}",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        message.add_field(name="​", value="\n".join(column_1))
        message.add_field(name="​", value="\n".join(column_2))
        await ctx.send(embed=message)

    @command(name="setnick", aliases=["newnick"])
    @has_permissions(manage_nicknames=True)
    async def moderation_setnick(self, ctx, member: Member = None, *, new_name: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}setnick [User] [New Name]` -> Gives a given user a new nickname.\n" +
                                                  "The nickname can not be longer than 32 characters.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)

        try:
            if len(new_name) > 32:
                new_name = new_name[:(len(new_name) - (len(new_name) - 32))]
            await member.edit(nick=new_name, reason=f"Member Nickname Changed | Done by -> {ctx.author}")
        except Forbidden:
            return await ctx.send("Was unable to change the nickname for that user.")

        message = utils.embed_message(title="Nickname Changed.",
                                      message=f"Changed {member}'s name to `{new_name}`.",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @command(name="whois", aliases=["userinfo"])
    @has_permissions(manage_messages=True)
    async def moderation_whois(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            member = ctx.author
        user_roles = []
        def check_boosted(user):
            if user.premium_since is None:
                return "No"
            else:
                return f"Since: {member.premium_since.day}/{member.premium_since.month}/{member.premium_since.year}"
        date_created = f"{member.created_at.day}/{member.created_at.month}/{member.created_at.year}"
        date_joined = f"{member.joined_at.day}/{member.joined_at.month}/{member.joined_at.year}"

        for role in member.roles:
            user_roles.append(f"{role.mention}")
        user_roles.pop(0)
        readable_roles = " ".join(user_roles)

        e = Embed(title=f"{member.name}'s Information", colour=Colour.blurple())
        e.set_thumbnail(url=member.avatar_url_as(size=64))

        e.add_field(name="Username:", value=f"{member}", inline=True)
        e.add_field(name="Date Created:", value=f"{date_created}", inline=True)
        e.add_field(name="Date Joined:", value=f"{date_joined}", inline=True)
        e.add_field(name="Is Boosting:", value=f"{check_boosted(member)}", inline=True)
        e.add_field(name=f"Roles: [{len(user_roles)}]",
                    value=f"{readable_roles}", inline=False)

        e.set_footer(icon_url=self.bot.user.avatar_url,
                     text=utils.random_message())

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(BasicModeration(bot))