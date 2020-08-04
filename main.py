import os
import asyncio

from decouple import config
from discord import Game, Status
from discord.ext import tasks
from discord.ext.commands import AutoShardedBot

from utils import db, basic_utilties as utils

# invoke_without_command=True

new_guilds = False

def get_status():
    return db.field("SELECT bot_status FROM bot_settings")

def get_premium():
    return db.field("SELECT * FROM bot_premium")

bot = AutoShardedBot(
    status=Status.dnd,
    activity=Game(name="Connecting..."),
    command_prefix=utils.get_prefix,
    case_insensitive=True,
    max_messages=100
)
bot.remove_command("help")
bot.owner_ids = {
    671777334906454026,
    200301688056315911
}
bot.premium_guilds = []

@tasks.loop(seconds=5)
async def get_premiums():
    await bot.wait_until_ready()
    bot.premium_guilds = utils.get_premium_guilds_ids()

@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

# Commands
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        utils.log(f"-> [MODULE] {file[:-3]} loaded.")

# Premium Modules
for file in os.listdir("./premium"):
    if file.endswith(".py"):
        bot.load_extension(f"premium.{file[:-3]}")
        utils.log(f"-> [PREMIUM MODULE] {file[:-3]} loaded.")

# Custom Modules
for file in os.listdir("./custom"):
    if file.endswith(".py"):
        bot.load_extension(f"custom.{file[:-3]}")
        utils.log(f"-> [CUSTOM MODULE] {file[:-3]} loaded.")

# Events
for file in os.listdir("./events"):
    if file.endswith(".py"):
        bot.load_extension(f"events.{file[:-3]}")
        utils.log(f"-> [EVENT] {file[:-3]} loaded.")

@bot.event
async def on_shard_ready(shard_id):
    utils.log(f"Shard Initialized -> {shard_id}")

@bot.event
async def on_ready():
    global new_guilds
    db.script_exec("./data/db/build.sql")
    if get_status() is None:
        db.execute("INSERT INTO bot_settings(bot_status) VALUES(?)", config("BOT_STATUS"))
        db.commit()
    await bot.change_presence(activity=Game(name=get_status()))
    utils.log(f"Logged in as -> {bot.user.name}")
    utils.log(f"Client ID -> {bot.user.id}")
    utils.log(f"Guild Count -> {len(bot.guilds)}")

    # Makes sure that all the guilds the bot is in are registered in the database
    # This may need to be used IF the bot is offline and gets added to new servers
    for guild in bot.guilds:
        get_guild = db.field("SELECT guild_id FROM guild_settings WHERE guild_id = ?", guild.id)
        if get_guild is None:
            new_guilds = True
            db.execute("INSERT INTO guild_settings(guild_id) VALUES(?)", guild.id)
            db.commit()
    if new_guilds:
        utils.log("-> Added new guild(s) to database.")
    # if get_premium() is not None:
    get_premiums.start()

bot.run(config("BOT_TOKEN"))
