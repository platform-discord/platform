from discord.ext import commands
import discord
import sqlite3
import json

config_json = open("config.json", "r")
config = json.load(config_json)
prefix = config["bot_config"]["prefix"]
bot_dev = config["bot_config"]["bot_dev"]

class Highlights(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        """
        Highlights cog
        Description: Once a message gets 3 Star reactions,
        it will be sent to a certain channel.
        ⭐
        """

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        highlight_reaction = "⭐"
        db = sqlite3.connect("my_db.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM highlight_settings WHERE guild_id = {payload.guild_id}")
        result_gid = cursor.fetchone()
        cursor.execute(f"SELECT * from highlight_count WHERE guild_id = {payload.guild_id}")
        result_counter = cursor.fetchall()
        if result_gid is None: return
        if payload.emoji.name == highlight_reaction:
            print("pass")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        hightlight_reaction = "⭐"
        db = sqlite3.connect("my_db.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT ")

    @commands.group(invoke_without_command=True, aliases=["highlight"])
    async def highlights(self, ctx):
        highlightEmbed = discord.Embed(title="Highlight Settings", colour=discord.Colour.dark_teal())

        highlightEmbed.add_field(
            name="Channel", 
            value=f"Sets the channel the highlights go into.\ne.g.`{prefix}highlights channel #highlights`",
            inline=False)
        # highlightEmbed.add_field(name="", value="", inline=False)
        # highlightEmbed.add_field(name="", value="", inline=False)

        highlightEmbed.set_footer(icon_url=self.bot.user.avatar_url,
                                  text=f"Developed by {bot_dev}")

        await ctx.send(embed=highlightEmbed)

    @highlights.command(name="channel")
    async def highlights_channel(self, ctx, channel: discord.TextChannel):
        db = sqlite3.connect("my_db.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM highlight_settings WHERE guild_id = {ctx.guild.id}")
        result_chanid = cursor.fetchone()
        if result_chanid is None:
            sql = ("INSERT INTO highlight_settings(guild_id, channel_id) VALUES(?, ?)")
            val = (ctx.guild.id, channel.id)
        elif result_chanid is not None:
            sql = ("UPDATE highlight_settings SET channel_id = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        await ctx.send(f"You have now set {channel.mention} to be the highlights channel.")
        cursor.close()
        db.close()

def setup(bot):
    bot.add_cog(Highlights(bot))
