import discord
from discord.ext import commands
import json
import sqlite3

s_crib = 692603241665527838
chnl_id = 693201108893433976
aaaaaaa = 724071088144908360

class SCrib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def confirm(self, ctx):
        print(ctx.guild.id)
        print(s_crib)
        if str(ctx.guild.id) != str(s_crib):
            return
        def check(m):
            return m.author == ctx.author
        
        await ctx.send("> This is a private server where you should feel safe to share anything without\n> judgement or being attacked. This is a breather from toxicity in other big\n> servers. **__Everything said here stays here, and if you try to use anything said\n> here against anyone or bring drama into here you will be kicked__**, which\n> hopefully won't happen! Does this sound good?\n`Yes` or `No`")
        user_input = await self.bot.wait_for("message", timeout=10, check=check)
        user_input_str = str(user_input.content)
        sus_shawty_channel = self.bot.get_channel(id=aaaaaaa)

        if (user_input_str.lower() == "yes"):
            sus_shawty = discord.utils.get(ctx.guild.roles, name="Sus Shawty")
            await ctx.send(f"Please make your way to <#{chnl_id}>")
            await ctx.author.add_roles(sus_shawty, reason="Shawdy suuussss")
            await ctx.message.channel.purge(limit=50)
            await sus_shawty_channel.send(f"{ctx.author.mention} Please wait for a higher-up to verify you. Use `?notify` to notify them.")
            # await ctx.send("Make sure to do p!confirm")
        elif (user_input_str.lower() == "no"):
            await ctx.author.kick(reason="They said no")


def setup(bot):
    bot.add_cog(SCrib(bot))
