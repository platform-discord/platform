import discord
from discord.ext import commands

class Server_Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        ''' Server Creation Command '''

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def self_destruct(self, ctx):        
        for channel in ctx.guild.channels:
            await channel.delete(reason="Deleting all Channels")

        await ctx.guild.create_text_channel(name="general")

    @commands.command(name="build")
    @commands.has_permissions(administrator=True)
    async def create_server(self, ctx, *, server_name: str = None):
        guild = ctx.guild

        if server_name == None:
            server_name = "Server Template"

        admin_perms = discord.Permissions(administrator=True)
        staff_perms = discord.Permissions(attach_files=True, mute_members=True, deafen_members=True, move_members=True, manage_nicknames=True, manage_permissions=True, view_audit_log=True)
        default_perms = discord.Permissions(send_messages=False, read_messages=False, attach_files=False)
        member_perms = discord.Permissions(send_messages=True, read_messages=True, attach_files=True)

        await guild.create_role(name="Developer", colour=discord.Colour.from_rgb(162, 31, 42), permissions=admin_perms)
        await guild.create_role(name="Co-Owner", colour=discord.Colour.from_rgb(222, 30, 121), permissions=admin_perms)
        await guild.create_role(name="High Staff", colour=discord.Colour.from_rgb(242, 82, 46), permissions=staff_perms)
        await guild.create_role(name="Staff", colour=discord.Colour.from_rgb(242, 82, 46), permissions=staff_perms)
        await guild.create_role(name="Member", colour=discord.Colour.from_rgb(15, 92, 237), permissions=member_perms)

        informationOverwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False)
        }

        staffOverwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, add_reactions=False),
            discord.utils.get(guild.roles, name="Staff"): discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True)
        }

        highStaffOverwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, add_reactions=False),
            discord.utils.get(guild.roles, name="Staff"): discord.PermissionOverwrite(read_messages=False, send_messages=True, add_reactions=True),
            discord.utils.get(guild.roles, name="High Staff"): discord.PermissionOverwrite(read_messages=False, send_messages=True, add_reactions=True)
        }

        mainOverwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False, attach_files=False),
            discord.utils.get(guild.roles, name="Member"): discord.PermissionOverwrite(send_messages=True, read_messages=True, attach_files=True)
        }

        defaultRole = discord.utils.get(guild.roles, name="@everyone")
        await defaultRole.edit(mention_everyone=False, send_tts_messages=False)

        await ctx.send("Server is being set up, this may take a bit.")
        await ctx.message.channel.delete(reason="Setting up server")
        await guild.edit(name="Setting up server.")

        await guild.create_category(name="[ Information ]", overwrites=informationOverwrites)
        await guild.create_category(name="[ Staff Channels ]", overwrites=staffOverwrites)
        await guild.create_category(name="[ Main Channels ]", overwrites=mainOverwrites)
        await guild.create_category(name="[ Community Channels ]", overwrites=mainOverwrites)
        await guild.create_category(name="[ Voice Channels ]", overwrites=mainOverwrites)
        await guild.create_category(name="[ Logs ]", overwrites=staffOverwrites)

        informationCategory = discord.utils.get(guild.categories, name="[ Information ]")
        staffCategory = discord.utils.get(guild.categories, name="[ Staff Channels ]")
        mainCategory = discord.utils.get(guild.categories, name="[ Main Channels ]")
        comCategory = discord.utils.get(guild.categories, name="[ Community Channels ]")
        voiceCategory = discord.utils.get(guild.categories, name="[ Voice Channels ]")
        logsCategory = discord.utils.get(guild.categories, name="[ Logs ]")

        # Information Category
        await guild.create_text_channel(name="welcome", topic="Welcome channel, all system messages get put here.", category=informationCategory)
        await guild.create_text_channel(name="rules", topic="Read up on the servers rules, don't break them!", category=informationCategory)
        await guild.create_text_channel(name="announcements", topic="Server announcements will go here.", category=informationCategory)
        await guild.create_text_channel(name="giveaways", topic="Server giveaway announcements will go here!", category=informationCategory)

        # Staff Category
        await guild.create_text_channel(name="staff-announcements", topic="Staff announcements will go here", category=staffCategory)
        await guild.create_text_channel(name="staff-rules", topic="Staff rules will go here", category=staffCategory)
        await guild.create_text_channel(name="staff-chat", topic="Staff chat, usually cooler than general 😎", category=staffCategory)
        await guild.create_text_channel(name="staff-commands", topic="Staff commands go here", category=staffCategory)
        await guild.create_text_channel(name="high-staff", topic="Staff announcements will go here", category=staffCategory, overwrites=highStaffOverwrites)

        # General Category
        await guild.create_text_channel(name="general", topic="General discussion, come here to make friends and such", category=mainCategory)
        await guild.create_text_channel(name="commands", topic="Do your bot commands here", category=mainCategory)
        await guild.create_text_channel(name="memes", topic="Send your dankest memes here", category=mainCategory)

        # Community Category
        await guild.create_text_channel(name="face-reveal", topic="Get your face reveals sent here!", category=comCategory)
        await guild.create_text_channel(name="self-promo", topic="Self promotion goes here", category=comCategory)
        await guild.create_text_channel(name="nsfw", topic="NSFW Content and Commands go here", category=comCategory)

        # Voice Category
        await guild.create_voice_channel(name="[🌍] General", category=voiceCategory)
        await guild.create_voice_channel(name="[15] Slots", user_limit=15, category=voiceCategory)
        await guild.create_voice_channel(name="[10] Slots", user_limit=10, category=voiceCategory)
        await guild.create_voice_channel(name="[8] Slots", user_limit=8, category=voiceCategory)
        await guild.create_voice_channel(name="[8] Slots", user_limit=8, category=voiceCategory)
        await guild.create_voice_channel(name="[5] Slots", user_limit=5, category=voiceCategory)
        await guild.create_voice_channel(name="[5] Slots", user_limit=5, category=voiceCategory)
        await guild.create_voice_channel(name="[3] Slots", user_limit=3, category=voiceCategory)
        await guild.create_voice_channel(name="[3] Slots", user_limit=3, category=voiceCategory)
        await guild.create_voice_channel(name="[2] Slots", user_limit=2, category=voiceCategory)
        await guild.create_voice_channel(name="[2] Slots", user_limit=2, category=voiceCategory)
        await guild.create_voice_channel(name="[20] Music", user_limit=20, category=voiceCategory)

        # Logs Category
        await guild.create_text_channel(name="staff-logs", category=logsCategory)
        await guild.create_text_channel(name="deleted-message-logs", category=logsCategory)
        await guild.create_text_channel(name="ban-logs", category=logsCategory)
        await guild.create_text_channel(name="user-logs", category=logsCategory)

        channel = discord.utils.get(ctx.guild.channels, name="welcome")
        await ctx.guild.edit(system_channel=discord.utils.get(guild.channels, name="welcome"))
        serverInvite = await channel.create_invite(max_age=0, max_uses=0, temporary=False, unique=True, reason="Server Setup")
        await guild.edit(name=server_name, verification_level=discord.VerificationLevel.medium)

        await channel.send(f"Server is done being set up.\nPermanent invite link: {serverInvite.url}")

def setup(bot):
    bot.add_cog(Server_Setup(bot))
