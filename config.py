import os
from typing import List

API_ID = int(os.getenv("API_ID", "22148722"))
API_HASH = os.getenv("API_HASH", "8ec84a1a32560fc1512f89a767d07c8e")
BOT_TOKEN = os.getenv("BOT_TOKEN", "6953624637:AAGpA7YsBvG9Y9tUplfS_kAJfTO-SE-2rkk")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://bajwa:bajwa@cluster0.aseiiq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID", "-1002454896752"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "1137799257"))
LOG_CHNL = int(os.getenv("LOG_CHNL", "-1002454896752"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "aswynps") 
IS_FSUB = bool(os.environ.get("FSUB", True))
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1002454896752").split()))
DATABASE_CHANNEL_LOG = int(os.getenv("DATABASE_CHANNEL_ID", "-1002454896752"))
FREE_VIDEO_DURATION = int(os.getenv("FREE_VIDEO_DURATION", "99999"))


FORCE_MSG = """<b><blockquote>⚠ Hᴇʏ, {mention} ×</blockquote>
Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ. Pʟᴇᴀsᴇ ʙᴇ sᴜʀᴇ ᴛᴏ ᴊᴏɪɴ ᴀʟʟ ᴛʜᴇ ᴄʜᴀɴɴᴇʟs ᴘʀᴏᴠɪᴅᴇᴅ ʙᴇʟᴏᴡ, ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ.. !</b>"""

PREMIUM_MSG = """
<b>Premium Plans</b>

Rear videos

Contact to upgrade!
"""