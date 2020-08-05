import asyncio

from discord.ext import tasks
from discord.ext.commands import Cog, group

from utils import db, basic_utilties as utils


async def check_free_slot_note(user_id):
    notes = db.record(f"SELECT note_one, note_two, note_three FROM user_notes WHERE user_id = {user_id}")
    note_list = ["note_one", "note_two", "note_three"]
    if notes[0] is None: return note_list[0]
    if notes[1] is None: return note_list[1]
    if notes[2] is None: return note_list[2]
    else:
        raise Exception


class Notes(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ""
        self.check_reminders.start()

    @tasks.loop(seconds=86400)
    async def check_reminders(self):
        await self.bot.wait_until_ready()
        mutes = db.records(f"SELECT * FROM user_notes")
        for record in mutes:
            is_reminder_enabled = db.field(f"SELECT reminder FROM user_notes WHERE user_id = {record[0]}")
            if is_reminder_enabled == 1:
                user = self.bot.get_user(record[0])
                note_one = db.field(f"SELECT note_one FROM user_notes WHERE user_id = {record[0]}")
                note_two = db.field(f"SELECT note_two FROM user_notes WHERE user_id = {record[0]}")
                note_three = db.field(f"SELECT note_three FROM user_notes WHERE user_id = {record[0]}")
                notes = f"""
                Note One:
                ```
                {note_one}
                ```
                Note Two:
                ```
                {note_two}
                ```
                Note Three:
                ```
                {note_three}
                ```
                """
                message = utils.embed_message(title="Your Notes",
                                              message=notes,
                                              footer_icon=self.bot.user.avatar_url,
                                              footer_text=utils.random_message())
                await user.send(embed=message)

    @group(name="notes", invoke_without_command=True)
    async def utility_notes(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        message = utils.embed_message(title="Notes",
                                      message="**Here you can set personal notes to yourself, you have the option to be reminded every 24 hours as well.**\n" +
                                              "*Don't store information that is too personal here*\n\n" +
                                              f"`{self.prefix}notes add [Text]` -> Adds a note to one of your available 3 slots.\n" +
                                              f"`{self.prefix}notes remove [1, 2 or 3]` -> Removes a note according to the slot you choose.\n" +
                                              f"`{self.prefix}notes view` -> Sends a DM of all your current notes you have.\n" +
                                              f"`{self.prefix}notes reminder` -> Sends a DM of all your notes every 24 hours.",
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.send(embed=message)

    @utility_notes.command(name="reminder")
    async def utility_notes_reminder(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        await ctx.send("Here are the options for reminders: Yes / No / Off")
        def check(m):
            return m.author.id == ctx.author.id
        try:
            wait_for_reply = await self.bot.wait_for("message", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(f"{ctx.author.mention} you ran out of time to answer.")
        else:
            user_reply = wait_for_reply.content.lower()
            if user_reply == "off":
                check_if_in_db = db.field(f"SELECT reminder FROM user_notes WHERE user_id = ?", ctx.author.id)
                if check_if_in_db is None:
                    return await ctx.send("You do not have reminders on.")
                db.execute(f"UPDATE user_notes SET reminder = ? WHERE user_id = ?", None, ctx.author.id)
                db.commit()
                return await ctx.send("Turned off reminders for you.")
            if user_reply == "yes":
                db.execute(f"UPDATE user_notes SET reminder = ? WHERE user_id = ?", 1, ctx.author.id)
                db.commit()
                return await ctx.send("⏱ You've enabled reminders! The bot will DM you every 24 hours.")
            if user_reply != "yes":
                return await ctx.send("Ok, won't give you reminders.")


    @utility_notes.command(name="add")
    async def utility_notes_add(self, ctx, *, note: str = None):
        await ctx.message.delete()
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if note is None:
            return await ctx.send("You must provide something to put into your notes.")
        is_user_in_db = db.field(f"SELECT user_id FROM user_notes WHERE user_id = ?", ctx.author.id)

        if is_user_in_db is None:
            db.execute(f"INSERT INTO user_notes(user_id) VALUES(?)", ctx.author.id)
            db.commit()
            try:
                free_note_slot = await check_free_slot_note(ctx.author.id)
            except Exception:
                return await ctx.send(f"You do not have a free slot in your notes. Do `{self.prefix}notes remove` to free some space.")
            else:
                db.execute(f"UPDATE user_notes SET ? = ? WHERE user_id = ?", free_note_slot, note, ctx.author.id)
                db.commit()
                return await ctx.send(f"Your note has been saved. Do `{self.prefix}notes view` to view all of your current notes.")

        try:
            free_note_slot = await check_free_slot_note(ctx.author.id)
        except Exception:
            return await ctx.send(f"You do not have a free slot in your notes. Do `{self.prefix}notes remove` to free some space.")
        else:
            db.execute(f"UPDATE user_notes SET ? = ? WHERE user_id = ?", free_note_slot, note, ctx.author.id)
            db.commit()
            await ctx.send(f"Your note has been saved. Do `{self.prefix}notes view` to view all of your current notes.")

    @utility_notes.command(name="remove")
    async def utility_notes_remove(self, ctx, note: int = None):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        if note is None:
            return await ctx.send("You must enter a note 1-3 to remove.")
        if note > 3:
            return await ctx.send("You must enter a note 1-3 to remove.")
        note_str = ""
        if note == 1: note_str = "note_one"
        if note == 2: note_str = "note_two"
        if note == 3: note_str = "note_three"
        check_note_exists = db.field(f"SELECT {note_str} FROM user_notes WHERE user_id = {ctx.author.id}")
        if check_note_exists is None:
            return await ctx.send("That slot is not filled with something currently.")
        db.execute(f"UPDATE user_notes SET {note_str} = ? WHERE user_id = ?", None, ctx.author.id)
        db.commit()
        await ctx.send("Successfully removed that note from your account.")

    @utility_notes.command(name="view")
    async def utility_notes_view(self, ctx):
        self.prefix = utils.get_guild_prefix(ctx.guild.id)
        note_one = db.field(f"SELECT note_one FROM user_notes WHERE user_id = ?", ctx.author.id)
        note_two = db.field(f"SELECT note_two FROM user_notes WHERE user_id = ?", ctx.author.id)
        note_three = db.field(f"SELECT note_three FROM user_notes WHERE user_id = ?", ctx.author.id)
        notes = f"""
        Note One:
        ```
        {note_one}
        ```
        Note Two:
        ```
        {note_two}
        ```
        Note Three:
        ```
        {note_three}
        ```
        """
        message = utils.embed_message(title="Your Notes",
                                      message=notes,
                                      footer_icon=self.bot.user.avatar_url,
                                      footer_text=utils.random_message())
        await ctx.author.send(embed=message)
        await ctx.send("You have been sent a DM with your notes.")

def setup(bot):
    bot.add_cog(Notes(bot))