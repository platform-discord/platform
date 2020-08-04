from discord.ext.commands import Cog

from utils import db, basic_utilties as utils

class VerificationEvent(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_message_delete(self, payload):
        check_message_id = db.field(f"SELECT message_id FROM guild_verification WHERE guild_id = {payload.guild_id}")

        if check_message_id is None:
            return

        db.execute(f"DELETE FROM guild_verification WHERE guild_id = {payload.guild_id}")
        db.commit()
        utils.log("Removed guild from verification table.")

def setup(bot):
    bot.add_cog(VerificationEvent(bot))