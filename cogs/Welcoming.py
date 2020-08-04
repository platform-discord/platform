import asyncio

from discord import TextChannel
from discord.ext.commands import Cog, command, has_permissions, group

from utils import basic_utilties as utils, db


class Welcoming(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""
        '''
        Welcoming Cog
        -------------
        Welcome users to guild if set
        '''

    @group(name="welcoming", aliases=["welcome"], invoke_without_command=True)
    @has_permissions(manage_guild=True)
    async def management_welcoming(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title="Welcoming Commands",
                                      message=f"`{self.prefix}welcoming channel [Text Channel]` -> Sets the text channel for welcome messages to go to.\n" +
                                              f"`{self.prefix}welcoming message [Message]` -> Sets the message for when someone joins the server.\n" +
                                              "E.g. " + self.prefix + "welcoming message welcome {mention} to {server}, enjoy your stay!\n" +
                                              f"`{self.prefix}welcoming reset` -> Resets the channel and message so new welcomes won't be sent there.",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @management_welcoming.command(name="channel")
    @has_permissions(manage_guild=True)
    async def management_welcoming_channel(self, ctx, channel: TextChannel = None):
        if channel is None:
            return await ctx.send("You must provide a channel for messages to go to.")
        check_if_in_db = db.field(f"SELECT guild_id FROM guild_welcome WHERE guild_id = {ctx.guild.id}")
        if check_if_in_db is None:
            db.execute(f"INSERT INTO guild_welcome(guild_id, welcome_channel_id) VALUES(?, ?)", ctx.guild.id, channel.id)
            db.commit()
            await ctx.send(f"Successfully set your welcome messages to go to -> {channel.mention}")
        elif check_if_in_db is not None:
            db.execute(f"UPDATE guild_welcome SET welcome_channel_id = ? WHERE guild_id = ?", channel.id, ctx.guild.id)
            db.commit()
            await ctx.send(f"Successfully updated your welcome messages to go to -> {channel.mention}")

    @management_welcoming.command(name="message")
    @has_permissions(manage_guild=True)
    async def management_welcoming_message(self, ctx, *, welcome_message: str = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if welcome_message is None:
            return await ctx.send("Your welcome message can't be nothing.")
        check_if_in_db = db.field(f"SELECT guild_id FROM guild_welcome WHERE guild_id = {ctx.guild.id}")
        if check_if_in_db is None:
            db.execute(f"INSERT INTO guild_welcome(guild_id, welcome_message) VALUES(?, ?)", ctx.guild.id, welcome_message)
            db.commit()
            await ctx.send(f"Successfully set your welcome message to -> `{welcome_message}`")
        if check_if_in_db is not None:
            db.execute(f"UPDATE guild_welcome SET welcome_message = ? WHERE guild_id = ?", welcome_message, ctx.guild.id)
            db.commit()
            await ctx.send(f"Successfully updated your welcome message to -> `{welcome_message}`")

    @management_welcoming.command(name="reset")
    @has_permissions(manage_guild=True)
    async def management_welcome_reset(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        def check(m):
            return m.author == ctx.author and m.guild.id == ctx.guild.id
        await ctx.send("Please reply with `yes` to reset the message and channel or `no` to not reset them.")
        try:
            wait_for_user_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(f"You did not reply in time! {ctx.author.mention}")
        else:
            user_reply = wait_for_user_reply.content.lower()
            if user_reply == "yes":
                db.execute(f"DELETE FROM guild_welcome WHERE guild_id = {ctx.guild.id}")
                db.commit()
                await ctx.send("Successfully reset your settings.")
            else:
                await ctx.send("Aborting, won't reset!")


def setup(bot):
    bot.add_cog(Welcoming(bot))