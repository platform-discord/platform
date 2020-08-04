import discord
from discord.ext import commands
import json
import sqlite3

config_json = open("config.json", "r")
config = json.load(config_json)
prefix = config["bot_config"]["prefix"]
bot_dev = config["bot_config"]["bot_dev"]


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        """
        Support Commands Cog
        """

    @commands.group()
    async def birthday(self, ctx):
        birthday_embed = discord.Embed(
            title="Birthday Settings",
            description="Set up your own birthday stuff here!",
            colour=discord.Colour.dark_teal()
        )

def setup(bot):
    bot.add_cog(Birthdays(bot))
