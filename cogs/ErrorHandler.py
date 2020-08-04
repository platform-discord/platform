from typing import Optional

from discord import Forbidden, Message, NotFound
from discord.ext import commands
from discord.ext.commands import Cog

from utils import basic_utilties as utils

class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored_errors = (commands.CommandNotFound,)

        if isinstance(error, ignored_errors):
            return

        setattr(ctx, "original_author_id", getattr(ctx, "original_author_id", ctx.author.id))
        owner_reinvoke_errors = (
            commands.MissingAnyRole, commands.MissingPermissions,
            commands.MissingRole, commands.CommandOnCooldown, commands.DisabledCommand,
        )

        if ctx.original_author_id in self.bot.owner_ids and isinstance(error, owner_reinvoke_errors):
            return await ctx.reinvoke()

        # Discord Forbidden, usually if bot doesn't have permissions

        # Command is on Cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            message = utils.embed_message(title="Command on Cooldown.",
                                          message=f"This command is on cooldown. **`{int(error.retry_after)}` seconds**",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message, delete_after=2)

        # Missing argument
        elif isinstance(error, commands.MissingRequiredArgument):
            message = utils.embed_message(title="Missing Argument.",
                                          message=f"You're missing the required argument: `{error.param.name}`",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message, delete_after=2)

        # Missing Permissions
        elif isinstance(error, commands.MissingPermissions):
            message = utils.embed_message(title="Missing Permissions.",
                                          message=f"You're missing the required permission: `{error.missing_perms[0]}`",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message, delete_after=2)

        # Missing Permissions
        elif isinstance(error, commands.BotMissingPermissions):
            message = utils.embed_message(title="Bot is Missing Permissions.",
                                          message=f"Platform is missing the required permission: `{error.missing_perms[0]}`",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message, delete_after=2)

        # Forbidden
        elif isinstance(error, Forbidden):
            message = utils.embed_message(title="Unable to complete action.",
                                          message=f"I was unable to complete this action, this is most likely due to permissions.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message, delete_after=2)

        # User who invoked command is not owner
        elif isinstance(error, commands.NotOwner):
            message = utils.embed_message(title="Unable to complete action.",
                                          message=f"You must be the owner of the bot to run this.",
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text=utils.random_message())
            return await ctx.send(embed=message, delete_after=2)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))