import os
from typing import List
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
LOG_CHNL = int(os.getenv("LOG_CHNL"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
IS_FSUB = os.getenv("FSUB", "True").lower() in ("true", "1", "yes")
AUTH_CHANNELS: List[int] = list(map(int, os.getenv("AUTH_CHANNEL", "").split(",")))
DATABASE_CHANNEL_LOG = int(os.getenv("DATABASE_CHANNEL_LOG"))
FREE_VIDEO_DURATION = int(os.getenv("FREE_VIDEO_DURATION"))

FORCE_MSG = os.getenv("FORCE_MSG")
PREMIUM_MSG = os.getenv("PREMIUM_MSG")
