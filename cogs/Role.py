from discord import Member, Embed
from discord.colour import Colour
from discord.ext.commands import Cog, MissingPermissions, MemberConverter
from discord.ext.commands import group
from discord.ext.commands import has_permissions

from utils import basic_utilties as utils


class Role(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""
        self.mr_ids = [668232158862639134,
                       622258457785008150,
                       735699294765711431,
                       735699295688327280,
                       735699298292990048]

    @group(name="role", invoke_without_command=True)
    @has_permissions(manage_roles=True)
    async def role_role(self, ctx, user: Member = None, *roles: str):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        """
            Give or take someones role
            Delete or add a role.
            Rename or Recolour a role.
        """
        if user is None or len(roles) == 0:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message=f"`{self.prefix}role [User] [Role]` -> Adds or Removes a role to/from a user.\n" +
                                          f"*To give or take multiple roles just separate them with spaces, to input a role with a space, wrap it in `\"`\n" +
                                          f"E.g. `{self.prefix}role kal#1806 \"Role One\" Role2`*\n" +
                                          f"`{self.prefix}role add [Role Name]` -> Creates a new role with a given name.\n" +
                                          f"`{self.prefix}role del [Role Name]` -> Deletes a given role\n" +
                                          f"`{self.prefix}role name [Role] [New Role Name]` -> Gives a role a new name.\n" +
                                          f"`{self.prefix}role colo(u)r [Role] [Hex Colour]` -> Give a role a new colour.\n" +
                                          f"`{self.prefix}role info [Role]` -> Gives information about a given role.",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)

        modifiers = []

        for role in roles:
            role = await utils.find_roles(ctx.guild, role)
            if role.id in self.mr_ids: return
            if role in user.roles:
                modifiers.append(f"-{role.mention}")
                await user.remove_roles(role, reason=f"Role Removed by -> {ctx.author}")
            else:
                modifiers.append(f"+{role.mention}")
                await user.add_roles(role, reason=f"Role Added by -> {ctx.author}")

        message = utils.embed_message(title="Updated Member Roles",
                                      message=f"Updated Roles for {user.mention} -> {' '.join(modifiers)}",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @role_role.command(name="add")
    @has_permissions(manage_roles=True)
    async def role_add(self, ctx, *, name: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if name is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="The correct format for this command is:\n" +
                                                  f"```\n{self.prefix}role add [New Role Name]```",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        new_role = await ctx.guild.create_role(name=name, reason=f"Role Created by -> {ctx.author}")
        message = utils.embed_message(title="Role Created.",
                                      message=f"{new_role.mention} has been created by -> {ctx.author.mention}",
                                      footer_icon=self.bot.user.avatar_url)
        await ctx.send(embed=message)

    @role_role.command(name="del")
    @has_permissions(manage_roles=True)
    async def role_del(self, ctx, *, name: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if name is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="The correct format for this command is:\n" +
                                                  f"```\n{self.prefix}role del [Role Name]```",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        role_to_delete = await utils.find_roles(ctx.guild, name)
        if role_to_delete is None:
            return await ctx.send("Role was not found.")
        message = utils.embed_message(title="Role Deleted.",
                                      message=f"`{role_to_delete.name}` has been deleted by -> {ctx.author.mention}",
                                      footer_icon=self.bot.user.avatar_url)
        await role_to_delete.delete(reason=f"Deleted by -> {ctx.author.mention}")
        await ctx.send(embed=message)

    @role_role.command(name="name")
    @has_permissions(manage_roles=True)
    async def role_name(self, ctx, cur_role: str = None, *, cur_role_new_name: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if cur_role is None or cur_role_new_name is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="The correct format for this command is:\n" +
                                                  f"```\n{self.prefix}role name [Role] [New Role Name]```",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        role = await utils.find_roles(ctx.guild, cur_role)
        if role is None:
            return await ctx.send("Role was not found.")
        message = utils.embed_message(title="Role Updated.",
                                      message=f"Changed role name from `{role.name}` -> `{cur_role_new_name}`",
                                      footer_icon=self.bot.user.avatar_url)
        await role.edit(name=cur_role_new_name, reason=f"Changed By -> {ctx.author}")
        await ctx.send(embed=message)

    @role_role.command(name="colour", aliases=["color"])
    @has_permissions(manage_roles=True)
    async def role_colour(self, ctx, role: str = None, colour: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if role is None or colour is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="The correct format for this command is:\n" +
                                                  f"```\n{self.prefix}role colo(u)r Owner #0123ff```",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)

        colour_too_long = utils.embed_message(title="Incorrect Syntax.",
                                      message="The colour must be 6 digits.",
                                      footer_icon=self.bot.user.avatar_url)

        if colour.startswith("#"): colour = colour[1:]
        if len(colour) > 6:
            return await ctx.send(embed=colour_too_long)
        role = await utils.find_roles(ctx.guild, role)
        if role is None:
            return await ctx.send("Role was not found.")
        colour = utils.hex_to_rgb(colour)
        message = utils.embed_message(title="Role Updated.",
                                      message=f"Updated {role.mention}'s colour -> {colour}",
                                      footer_icon=self.bot.user.avatar_url)
        await role.edit(colour=Colour.from_rgb(colour[0], colour[1], colour[2]), reason=f"Changed By -> {ctx.author}")
        await ctx.send(embed=message)

    @role_role.command(name="info")
    @has_permissions(manage_messages=True)
    async def role_info(self, ctx, role: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if role is None:
            message = utils.embed_message(title="Incorrect Syntax.",
                                          message="The correct format for this command is:\n" +
                                                  f"```\n{self.prefix}role info [Role]```",
                                          footer_icon=self.bot.user.avatar_url)
            return await ctx.send(embed=message)
        role = await utils.find_roles(ctx.guild, role)
        if role is None:
            return await ctx.send("Role was not found.")
        role_colour = (role.colour.r, role.colour.g, role.colour.b)
        role_colour_hex = '#%02x%02x%02x' % role_colour
        e = Embed(title=f"{role.name} Information.",
                  colour=Colour.from_rgb(role.colour.r, role.colour.g, role.colour.b))
        e.set_footer(text=utils.random_message(), icon_url=self.bot.user.avatar_url)

        e.add_field(name="Role ID",
                    value=f"{role.id}")

        e.add_field(name="Role Mention",
                    value=f"`{role.mention}`")

        e.add_field(name="Role Creation Date",
                    value=f"{role.created_at.day}/{role.created_at.month}/{role.created_at.year}")

        e.add_field(name="Role Position",
                    value=f"{role.position}")

        e.add_field(name="Role Hoisted",
                    value=f"{role.hoist}")

        e.add_field(name="Role Colour",
                    value=f"{role_colour_hex}")

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Role(bot))