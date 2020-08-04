import discord
from discord.ext import commands
import json

config_json = open("config.json", "r")
config = json.load(config_json)
prefix = config["bot_config"]["prefix"]
bot_dev = config["bot_config"]["bot_dev"]

def add_channel(channel_id):
    with open("channel_ids.txt", "a") as f:
        f.write(channel_id)

def remove_channel(channel_id):
    with open("channel_ids.txt", "r+") as f:
        data = ''.join([i for i in f if not i.lower().startswith(str(channel_id))])
        f.seek(0)
        f.write(data)
        f.truncate()


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def create_global(self, ctx):
        global_chat = await ctx.guild.create_text_channel("global-chat", category=ctx.message.channel.category)
        add_channel(str(global_chat.id))
        await ctx.send(f"Created <#{global_chat.id}> and added it to the global chat list") 
        await global_chat.send(f"Before you delete this channel please do\n{prefix}disconnect\nThanks for using {self.bot.user.name} :)")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def connect(self, ctx):
        add_channel(str(ctx.message.channel.id) + "\n")
        await ctx.send("Please make sure before you delete this channel to do `p!disconnect` thanks!")
        await ctx.send("Channel has been added to global chat list.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def disconnect(self, ctx):
        remove_channel(str(ctx.message.channel.id))
        await ctx.send("Channel has been removed from the global chat list.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user: return
        f = open("channel_ids.txt", "r")
        content = f.readlines()
        content = [x.strip() for x in content]
        for channel in content:
            if str(message.channel.id) in content:
                if str(message.channel.id) != channel:
                    send_to = self.bot.get_channel(int(channel))
                    await send_to.send(f"{message.guild.name} | {message.author} > {message.content}")

def setup(bot):
    bot.add_cog(GlobalChat(bot))
