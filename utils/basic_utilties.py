import json
import re
import time
import typing
import urllib
from typing import Optional

import discord
from discord import Embed
from discord.ext.commands import when_mentioned_or
from discord.ext.commands import bot

from . import db

from random import choice

def log(*args):
    print(f"{time.strftime('%I:%M:%S')} | {' '.join(map(str, args))}")

def is_guild_premium(guild_id):
    guild = db.field(f"SELECT guild_id FROM bot_premium WHERE guild_id = {guild_id}")
    if guild is None:
        return False
    else:
        return True

def get_premium_guilds():
    guilds = db.records("SELECT * FROM bot_premium")
    return guilds

def get_premium_guilds_ids():
    guilds = db.column("SELECT guild_id FROM bot_premium")
    return guilds

def get_premium_guild(guild):
    guild = db.record(f"SELECT * FROM bot_premium WHERE guild_id = {guild.id}")
    return guild

def random_message():
    with open("messages.txt", "r", encoding="UTF-8") as f:
        message = choice(f.readlines())
    return message

def get_prefix(bot, message):
    prefix = db.field("SELECT prefix FROM guild_settings WHERE guild_id = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)

def get_guild_prefix(guild_id):
    prefix = db.field("SELECT prefix FROM guild_settings WHERE guild_id = ?", guild_id)
    return prefix

async def is_target_staff(ctx, user) -> str:
    ch = ctx.message.channel
    permissions = ch.permissions_for(user).manage_messages
    return permissions

async def urban_def(urban_args) -> dict:
    query = str(urban_args)
    if " " in query:
        query = query.replace(" ", "-")
    url = "http://api.urbandictionary.com/v0/define?term=%s" % (query)

    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    definition = data["list"][0]["definition"]

    return definition

async def urban_xmp(urban_args) -> dict:
    query = str(urban_args)
    if " " in query:
        query = query.replace(" ", "-")
    url = "http://api.urbandictionary.com/v0/define?term=%s" % (query)

    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    example = data["list"][0]["example"]

    return example

async def get_user_banned(guild, name_arg):
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if name_arg.lower().startswith(user.name.lower()):
            member_to_unban = discord.Object(id=user.id)
            return member_to_unban
    return None

async def find_roles(guild, role_arg) -> Optional[typing.Any]:
    if re.fullmatch('<@&[0-9]{15,}>', role_arg) is not None:
        return guild.get_role(int(role_arg[3:-1]))
    if role_arg.isnumeric():
        return guild.get_role(int(role_arg))
    for role in guild.roles:
        if role.name.lower().startswith(role_arg.lower()):
            return role
    return None

def hex_to_rgb(h) -> tuple:
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def split_list(a_list) -> typing.Tuple[typing.Any, typing.Any]:
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]

def embed_message(*, title: str = None,
                  message: str = None,
                  colour: discord.Colour = discord.Colour.blurple(),
                  footer_text: str = "Developed by -> kal#1806",
                  footer_icon: str = "",
                  url: str = None,
                  thumbnail: str = "") -> Embed:
    """
    Purpose
    -------
    Returns a basic embed with a given title,
    message which is the description and colour if one is set.
    :rtype: object
    """
    new_embed = Embed(
        title=title,
        description=message,
        colour=colour,
        url=url
    )
    new_embed.set_footer(text=footer_text, icon_url=footer_icon)
    new_embed.set_thumbnail(url=thumbnail)
    return new_embed