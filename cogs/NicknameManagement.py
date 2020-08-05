from discord import Member, Forbidden
from discord.ext.commands import Cog, group, has_permissions, command, MissingPermissions
from utils import db, basic_utilties as utils

class NicknameManagement(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""
        #self.prefix = utils.get_guild_prefix(ctx.guild.id)

    @command(name="nickban", invoke_without_command=True)
    @has_permissions(manage_messages=True)
    async def nicknames_ban(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            message = f"""
            `{self.prefix}nickban [User]` -> Stops the user from changing their nickname
            """
            incorrect_syntax = utils.embed_message(title="Incorrect Syntax",
                                                   message=message,
                                                   footer_icon=self.bot.user.avatar_url,
                                                   footer_text=utils.random_message())
            return await ctx.send(embed=incorrect_syntax)
        check_if_staff = await utils.is_target_staff(ctx, member)
        if check_if_staff:
            message = utils.embed_message(message="❌ That user is a staff member",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message)
        check_if_in_db = db.field(f"SELECT member_id FROM guild_nick_bans WHERE guild_id = ?", ctx.guild.id)
        if check_if_in_db is not None:
            return await ctx.send("❌ That user is already nickbanned.")
        db.execute(f"INSERT INTO guild_nick_bans(guild_id, member_id) VALUES(?, ?)", ctx.guild.id, member.id)
        db.commit()
        try:
            await member.edit(nick="Nickname Violation")
        except Forbidden:
            return await ctx.send("❌ Could not change the nickname for this user, this may cause issues later on.")
        else:
            await ctx.send(f"✅ Successfully denied {member} from changing their nickname.")

    @command(name="unnickban")
    @has_permissions(manage_messages=True)
    async def nicknames_unban(self, ctx, member: Member = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if member is None:
            message = f"""
                    `{self.prefix}unnickban [User]` -> Unbans a user from changing their nickname
                    """
            incorrect_syntax = utils.embed_message(title="Incorrect Syntax",
                                                   message=message,
                                                   footer_icon=self.bot.user.avatar_url,
                                                   footer_text=utils.random_message())
            return await ctx.send(embed=incorrect_syntax)
        check_if_in_db = db.field(f"SELECT member_id FROM guild_nick_bans WHERE guild_id = {ctx.guild.id}")
        if check_if_in_db is None:
            return await ctx.send("❌ That user is not nickbanned.")
        db.execute(f"DELETE FROM guild_nick_bans WHERE guild_id = ? AND member_id = ?", ctx.guild.id, member.id)
        db.commit()
        await ctx.send(f"✅ Successfully unbanned {member} from changing their nickname.")

def setup(bot):
    bot.add_cog(NicknameManagement(bot))