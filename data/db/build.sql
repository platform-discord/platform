CREATE TABLE IF NOT EXISTS guild_settings(
	guild_id INTEGER PRIMARY KEY,
	prefix TEXT DEFAULT "p?",
	mute_role INTEGER
);
CREATE TABLE IF NOT EXISTS guild_verification(
    guild_id INTEGER PRIMARY KEY,
    message_id INTEGER,
    role_id INTEGER
);
CREATE TABLE IF NOT EXISTS bot_settings(
    bot_status TEXT DEFAULT "p?help | p?support"
);
CREATE TABLE IF NOT EXISTS guild_mutes(
    guild_id INTEGER,
    user_id INTEGER,
    unix_time INTEGER
);
CREATE TABLE IF NOT EXISTS bot_premium(
    guild_id INTEGER PRIMARY KEY,
    end_time INTEGER
);
CREATE TABLE IF NOT EXISTS guild_welcome(
    guild_id INTEGER PRIMARY KEY,
    welcome_channel_id INTEGER,
    welcome_message TEXT
);
CREATE TABLE IF NOT EXISTS guild_notable(
    guild_id INTEGER PRIMARY KEY,
    role_id INTEGER
);
CREATE TABLE IF NOT EXISTS guild_notable_members(
    guild_id INTEGER,
    member_id INTEGER,
    staff_id INTEGER
);
CREATE TABLE IF NOT EXISTS guild_ranks(
    guild_id INTEGER,
    member_id INTEGER,
    xp INTEGER,
    level INTEGER,
    xp_lock INTEGER
);
CREATE TABLE IF NOT EXISTS guild_rank_settings(
    guild_id INTEGER,
    channel_id INTEGER,
    enabled INTEGER
);
CREATE TABLE IF NOT EXISTS user_notes(
    user_id INTEGER PRIMARY KEY,
    note_one TEXT,
    note_two TEXT,
    note_three TEXT,
    reminder INTEGER
);
CREATE TABLE IF NOT EXISTS guild_nick_bans(
    guild_id INTEGER,
    member_id INTEGER
);
CREATE TABLE IF NOT EXISTS suggestion_blacklist(
    member_id INTEGER,
    reason TEXT
);
CREATE TABLE IF NOT EXISTS guild_reports(
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER
);