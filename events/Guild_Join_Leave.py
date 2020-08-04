from discord.ext.commands import Cog
import discord

from utils import db, basic_utilties as utils


class GuildEvents(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild):
        # Add guild to DB
        db.execute("INSERT INTO guild_settings(guild_id, prefix) VALUES(?, ?)", guild.id, "p?")
        db.commit()

        # Send a message to channel saying we got removed to a server
        logging_channel = self.bot.get_channel(710978375203946498)
        message = utils.embed_message(title="Added to Guild!",
                                      message=f"{guild.name} has added me to their guild with {len(guild.members)} members / Now in {len(self.bot.guilds)}")
        await logging_channel.send(embed=message)

    @Cog.listener()
    async def on_guild_remove(self, guild):
        # Remove guild from Database
        db.execute(f"DELETE FROM guild_settings WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_verification WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_mutes WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_notable WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_notable_members WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_welcome WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_ranks_settings WHERE guild_id = {guild.id}")
        db.execute(f"DELETE FROM guild_ranks WHERE guild_id = {guild.id}")
        db.commit()

        # Send a message to channel saying we got removed to a server
        logging_channel = self.bot.get_channel(710978375203946498)
        message = utils.embed_message(title="Removed from Guild",
                                      message=f"{guild.name} has removed me from their guild with {len(guild.members)} members / Now in {len(self.bot.guilds)}")
        await logging_channel.send(embed=message)

def setup(bot):
    bot.add_cog(GuildEvents(bot))
