from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors import ButtonUrlInvalid
from sendbot.db.mdb import mdb
from config import ADMIN_ID
from sendbot.modules.string_buttons import string_to_buttons
from sendbot import app

@app.on_message(filters.private & filters.user(ADMIN_ID))
async def admin_message_handler(client: Client, message: Message):
    admin_state = await mdb.get_admin_state(message.from_user.id)

    if admin_state == "add_caption":
        if message.text.lower() == '/cancel':
            await mdb.set_admin_state(message.from_user.id, None)
            await message.reply('Cancelled', quote=True)
            return

        await mdb.set_caption(message.text.markdown)
        await mdb.set_admin_state(message.from_user.id, None)
        await message.reply('Caption set successfully ✅', quote=True)

    elif admin_state == "add_buttons":
        if message.text.lower() == '/cancel':
            await mdb.set_admin_state(message.from_user.id, None)
            await message.reply('Cancelled', quote=True)
            return
        if "-" not in message.text:
            await message.reply('Wrong format! Try again.', quote=True)
            return

        try:
            given_buttons = await string_to_buttons(message.text)
            await message.reply('Preview:', reply_markup=InlineKeyboardMarkup(given_buttons))
            await mdb.set_buttons(message.text)
            await mdb.set_admin_state(message.from_user.id, None)
            await message.reply('Buttons set successfully ✅', quote=True)
        except ButtonUrlInvalid:
            await message.reply('Invalid URL format! Try again.', quote=True)
        except Exception as e:
            await message.reply(f"An error occurred: {e}", quote=True)

from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ButtonUrlInvalid
import asyncio.exceptions
from sendbot.db.mdb import mdb
db = mdb
from sendbot.modules.string_buttons import string_to_buttons
from config import ADMIN_ID

@app.on_message(filters.command("settings") & filters.private & filters.user(ADMIN_ID))
async def settings_handler(client: Client, message: Message):
    if getattr(client, "REQFSUB", False):
        reqfsub_button = InlineKeyboardButton("Disable Request ForceSub", callback_data="chng_req")
    else:
        reqfsub_button = InlineKeyboardButton("Enable Request ForceSub", callback_data="chng_req")

    buttons = [
        [InlineKeyboardButton("Manage Caption", callback_data="change_caption")],
        [InlineKeyboardButton("Manage Buttons", callback_data="change_buttons")],
        [reqfsub_button],
    ]

    await message.reply(
        "**⚙️ Global Settings**\n\n"
        "Here you can set a global caption and buttons for your bot.\n"
        "- Caption → Text that will be added to posts.\n"
        "- Buttons → Inline buttons that appear with posts.\n"
        "- ForceSub → Require users to join a channel before using the bot.",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.MARKDOWN
    )