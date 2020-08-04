import contextlib
import io
import json
import textwrap
import time
import traceback
import asyncio

import discord
from discord import Colour, Member
from discord.ext import tasks
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import is_owner

from utils import db, basic_utilties as utils


class Developer(Cog):
    def __init__(self, bot):
        self._last_result = None
        self.bot = bot
        self.check_premium.start()

    @tasks.loop(seconds=1)
    async def check_premium(self):
        await self.bot.wait_until_ready()
        guilds = utils.get_premium_guilds()
        for record in guilds:
            ends_at = record[1]
            ends_in = int(ends_at - time.time())
            guild = self.bot.get_guild(record[0])
            if ends_in < 0:
                db.execute(f"DELETE FROM bot_premium WHERE guild_id = {guild.id}")
                db.commit()

    @staticmethod
    def _cleanup_code(content):
        """Automatically removes code blocks from the code."""

        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            if content[-4] == '\n':
                return '\n'.join(content.split('\n')[1:-1])
            return '\n'.join(content.split('\n')[1:]).rstrip('`')

        # remove `foo`
        return content.strip('` \n')

    @command(name="todo")
    @is_owner()
    async def developer_todo(self, ctx, *, todo: str):
        await ctx.message.delete()
        channel = self.bot.get_channel(715597836670205996)
        todo_time = time.ctime(time.time())
        message =f"""
**TODO - {todo_time}**
{todo}
"""
        await channel.send(message)

    #suggestion_blacklist
    @command()
    @is_owner()
    async def suggest_blacklist(self, ctx, member: Member, *, reason: str = "None"):
        db.execute(f"INSERT INTO suggestion_blacklist(member_id, reason) VALUES(?, ?)", member.id, reason)
        db.commit()
        await ctx.message.add_reaction("\N{OK HAND SIGN}")

    @command()
    @is_owner()
    async def add_premium(self, ctx, guild_to_add_premium: int, end_time: int = 2147483646):
        if end_time != 2147483646:
            end_time = int(time.time() + (end_time * 86400))
        db.execute(f"INSERT INTO bot_premium(guild_id, end_time) VALUES(?, ?)", guild_to_add_premium, end_time)
        db.commit()
        end_date = time.ctime(end_time)
        await ctx.send(f"Successfully added {guild_to_add_premium} to the premium table. Ends at -> " +
                       f"{end_date}")

    @command()
    @is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @command()
    @is_owner()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @command()
    @is_owner()
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @command()
    @is_owner()
    async def ev(self, ctx, *, content: str):
        """Evaluates some Python code
        Gracefully stolen from Rapptz ->
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L72-L117"""

        # Make the environment
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'self': self,
        }
        env.update(globals())

        # Make code and output string
        content = self._cleanup_code(content)
        code = f'async def func():\n{textwrap.indent(content, "  ")}'

        # Make the function into existence
        stdout = io.StringIO()
        try:
            exec(code, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        # Grab the function we just made and run it
        func = env['func']
        try:
            # Shove stdout into StringIO
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            # Oh no it caused an error
            stdout_value = stdout.getvalue() or None
            message = utils.embed_message(message=f'```py\n{stdout_value}\n{traceback.format_exc()}\n```',
                                          colour=Colour.blurple(),
                                          footer_icon=self.bot.user.avatar_url,
                                          footer_text="Hey if you read this, you're cool \N{SMILING FACE WITH SUNGLASSES}")
            await ctx.send(embed=message)
        else:
            # Oh no it didn't cause an error
            stdout_value = stdout.getvalue() or None

            # Give reaction just to show that it ran
            await ctx.message.add_reaction("\N{OK HAND SIGN}")

            # If the function returned nothing
            if ret is None:
                # It might have printed something
                if stdout_value is not None:
                    message = utils.embed_message(message=f'```py\n{stdout_value}\n```',
                                                  colour=Colour.blurple(),
                                                  footer_icon=self.bot.user.avatar_url,
                                                  footer_text="Hey if you read this, you're cool \N{SMILING FACE WITH SUNGLASSES}")
                    await ctx.send(embed=message)
                return

            # If the function did return a value
            result_raw = stdout_value or ret  # What's returned from the function
            result = str(result_raw)  # The result as a string
            if result_raw is None:
                return
            text = f'```py\n{result}\n```'
            if type(result_raw) == dict:
                try:
                    result = json.dumps(result_raw, indent=4)
                except Exception:
                    pass
                else:
                    text = f'```json\n{result}\n```'
            if len(text) > 2000:
                await ctx.send(file=discord.File(io.StringIO(result), filename='ev.txt'))
            else:
                message = utils.embed_message(message=text,
                                              colour=Colour.blurple(),
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text="Hey if you read this, you're cool \N{SMILING FACE WITH SUNGLASSES}")
                await ctx.send(embed=message)


def setup(bot):
    bot.add_cog(Developer(bot))