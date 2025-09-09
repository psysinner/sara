
from pyrogram import *
from config import ADMIN_ID
from sendbot.db.mdb import mdb
from sendbot.db.udb import udb
from sendbot import app
import time

async def get_readable_time(seconds: int) -> str:
    time_data = []
    for unit, div in [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]:
        value, seconds = divmod(seconds, div)
        if value > 0 or unit == "s":
            time_data.append(f"{int(value)}{unit}")
    return " ".join(time_data)

@Client.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.delete()
        await message.reply_text("**🚫 You're not authorized to use this command...**")
        return
    video_count = await mdb.count_all_videos()
    total_users = await udb.get_all_users()
    bot_uptime = int(time.time() - app.START_TIME)
    uptime = await get_readable_time(bot_uptime)
    STATS = ">**🤖 Bot Statistics**\n\n"
    STATS += f"**Total Users: {len(total_users)}\n**"
    STATS += f"**Total Files in DB: {video_count}\n**"
    STATS += f"**BOT Uptime: {uptime}**"
    await message.reply_text(STATS)
