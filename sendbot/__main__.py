import asyncio
import importlib
from pathlib import Path
from pyrogram import idle
from sendbot import LOGGER, app
from sendbot.modules import ALL_MODULES
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10)
async def init():
    await app.start()
    plugins_path = Path("sendbot/modules")
    for module_path in plugins_path.glob("*.py"):
        module_name = module_path.stem
        importlib.import_module(f"sendbot.modules.{module_name}")
    LOGGER("sendbot.modules").info("Successfully imported all sendbot.modules.")
    await idle()
    await app.stop()
    LOGGER("sendbot").info("Stopping the bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())