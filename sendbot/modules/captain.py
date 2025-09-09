
from pyrogram import *
from config import ADMIN_ID, ADMIN_USERNAME
from sendbot.db.mdb import mdb
from sendbot.db.udb import udb
from sendbot import app
import time
from pyrogram.errors import ButtonUrlInvalid
from pyrogram import Client, filters
from pyrogram.types import *
from datetime import datetime
import pytz
from pyrogram.enums import ParseMode
db = mdb
from sendbot.modules.string_buttons import string_to_buttons
import asyncio

@Client.on_callback_query()
async def cb_handler(client, q: CallbackQuery):
    data = q.data

    if data == "close":
        await q.answer("Thanks for closing ❤️", show_alert=True)
        await q.message.delete()

    elif data == "help":
        await q.edit_message_text(
            text=f"""<b>This bot is specially designed for 18+ users and allows you to access content easily through simple commands.

You can use /getvideo to request an 18+ video and /myplan to check your current daily limit and subscription details.

Along with the free plan, we also offer premium plans,

» Silver
» Gold
» Diamond

which provide higher limits, faster access, and better features for a smoother experience.

Please note, this bot is strictly for adult users (18+) and you are using it at your own responsibility.

<a href="https://telegram.org/privacy">Terms and Conditions</a></b>""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("About", url="https://xyz.com")],
                [InlineKeyboardButton("Admin", callback_data="admincmds"),
                 InlineKeyboardButton("Home", callback_data="home")]]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

    elif data == "about":
        b = await client.get_me()
        await q.edit_message_text(
            text=f"""<b><blockquote>📄 Bot Info</blockquote>

» Bot Name - <a href='tg://user?id={b.id}'>{b.first_name}</a>
» Developer - <a href='https://t.me/{ADMIN_USERNAME}'>{ADMIN_USERNAME}</a>
» Updates - <a href='https://t.me/adulthub4all'>AdultHub4All</a>

<blockquote>⚙️ Bot Setup Details</blockquote>

» Version - V0.3
» Language - <a href='https://www.python.org/download/releases/3.0/'>Python3</a>
» Library - <a href='https://docs.pyrogram.org/'>Pyrogram</a>
» Database - <a href='https://www.mongodb.com/'>MongoDB</a>

<blockquote>⚠️ If you facing any error, Please Contact - <a href='https://t.me/{ADMIN_USERNAME}'>Support</a></blockquote>

<a href="https://telegram.org/privacy">Terms and Conditions</a></b>""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Home", callback_data="home"),
                 InlineKeyboardButton("Help", url="https://xyz.com")]]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

    elif data == "home":
        full_name = q.from_user.first_name + \
            (" " + q.from_user.last_name if q.from_user.last_name else "")
        h = datetime.now(pytz.timezone('Asia/Kolkata')).hour
        wish = "Good Morning" if 4 <= h < 12 else "Good Afternoon" if 12 <= h < 17 else "Good Evening" if 17 <= h < 20 else "Good Night"
        await q.edit_message_text(
            text=f"""<b>👋 {full_name}, {wish}

<blockquote expandable>This bot may contain 18+ content.
Please access it at your own risk.
The material may include explicit or graphic content that is not suitable for minors.</blockquote>

<a href="https://telegram.org/privacy">Terms and Conditions</a></b>""", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Buy Subscription", callback_data="pro")],
                 [InlineKeyboardButton("Help", url="https://xyz.com"), InlineKeyboardButton("About", url="https://xyz.com")], [InlineKeyboardButton("Close", callback_data="close")]]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)

    elif data == "pro":
        current_limits = await mdb.get_global_limits()
        PRIME_TXT = f"""<b><u>Free Plan:</u>

<blockquote expandable>» This free plan allows you only {current_limits['free_limit']} files per day.

» Videos must be less than 5 minutes in length.

» Free forever.</blockquote>

If you wish to upgrade, simply choose your preferred plan from the options below.

<a href="https://telegram.org/privacy">Terms and Conditions</a></b>"""
        await q.edit_message_text(
            PRIME_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('Silver Plan', callback_data='silver')],
                [InlineKeyboardButton('Gold Plan', callback_data='gold')],
                [InlineKeyboardButton('Diamond Plan', callback_data='diamond')],
                [InlineKeyboardButton('Back', callback_data='home'),
                InlineKeyboardButton('Close', callback_data='close')]
            ]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

    elif data == "silver":
        current_limits = await mdb.get_global_limits()
        await q.edit_message_text(
            text=f"""<b><u>Silver Plan</u>

» 1 Week - 25 INR
» This silver plan allows you {current_limits['prime_limit']} files per day.

<a href='https://files.catbox.moe/tu5hr1.jpg'>Click To Get QR</a>

<blockquote expandable>Note: Once you select a plan, it cannot be changed please choose carefully. Payments are non-refundable, so make sure to review everything before proceeding.</blockquote>

💬 Contact @{ADMIN_USERNAME} to upgrade your plan</b>""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Back", callback_data="pro")]]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)

    elif data == "gold":
        current_limits = await mdb.get_global_limits()
        await q.edit_message_text(
            text=f"""<b><u>Gold Plan</u>

» 15 Days - 40 INR
» This Gold plan allows you {current_limits['prime_limit']} files per day.

<a href='https://files.catbox.moe/tu5hr1.jpg'>Click To Get QR</a>

<blockquote expandable>Note: Once you select a plan, it cannot be changed please choose carefully. Payments are non-refundable, so make sure to review everything before proceeding.</blockquote>

💬 Contact @{ADMIN_USERNAME} to upgrade your plan</b>""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Back", callback_data="pro")]]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

    elif data == "diamond":
        current_limits = await mdb.get_global_limits()
        await q.edit_message_text(
            text=f"""<b><u>Diamond Plan</u>

» 1 Month - 60 INR
» This Diamond plan allows you {current_limits['prime_limit']} files per day.

<a href='https://files.catbox.moe/tu5hr1.jpg'>Click To Get QR</a>

<blockquote expandable>Note: Once you select a plan, it cannot be changed please choose carefully. Payments are non-refundable, so make sure to review everything before proceeding.</blockquote>

💬 Contact @{ADMIN_USERNAME} to upgrade your plan</b>""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Back", callback_data="pro")]]),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

    elif data == "admincmds":
        if q.from_user.id != ADMIN_ID:
            await q.answer("You are not my admin ❌", show_alert=True)
        else:
            t = """<b><u>⭐ Admin Commands</u>
                                      
» /setlimit — Increase the daily usage limit for any user (applies to both Free and Prime users).

» /maintenance — Toggle maintenance mode ON or OFF.

» /prime — Add a user to the Prime membership.

» /remove — Remove a user from Prime membership.

» /deleteall — Delete all videos from the database.

» /delete — Delete a specific video using its Telegram message ID.

» /broadcast — Send a message broadcast to all users.

» /ban — Ban a specific user.

» /unban — Unban a specific user.

» /stats — View detailed bot statistics.</b>"""
            await q.edit_message_text(t,
                                      reply_markup=InlineKeyboardMarkup(
                                          [[InlineKeyboardButton("Back", callback_data="help")]]))

    callback_query = q
    user_id = callback_query.from_user.id
    query = callback_query.data.lower()

    if query == "change_caption":
        caption = await db.get_caption()
        if caption:
            buttons = [
                [InlineKeyboardButton('Change Caption', callback_data='add_caption')],
                [InlineKeyboardButton('Remove Caption', callback_data='remove_caption')],
                [InlineKeyboardButton('⬅️ Back', callback_data='home')]
            ]
            await callback_query.edit_message_text(
                f'Current Caption is :\n\n{caption}\n\nUse below buttons to change or remove it.',
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            buttons = [
                [InlineKeyboardButton('Add Caption', callback_data='add_caption')],
                [InlineKeyboardButton('⬅️ Back', callback_data='home')]
            ]
            await callback_query.edit_message_text(
                f'No Caption set.\n\nUse below button to add it.',
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif query == "change_buttons":
        buttons = await db.get_buttons()
        if buttons:
            _buttons = [
                [InlineKeyboardButton('Change URL Buttons', callback_data='add_buttons')],
                [InlineKeyboardButton('Remove URL Buttons', callback_data='remove_buttons')],
                [InlineKeyboardButton('⬅️ Back', callback_data='home')]
            ]
            await callback_query.edit_message_text(
                f'Current Buttons are :\n\n`{buttons}`\n\nUse below buttons to change or remove them.',
                reply_markup=InlineKeyboardMarkup(_buttons)
            )
        else:
            _buttons = [
                [InlineKeyboardButton('Add Buttons', callback_data='add_buttons')],
                [InlineKeyboardButton('⬅️ Back', callback_data='home')]
            ]
            await callback_query.edit_message_text(
                f'No Buttons set.\n\nUse below button to add them.',
                reply_markup=InlineKeyboardMarkup(_buttons)
            )

    elif query == "add_caption":
        try:
            data = await client.ask(
                user_id,
                'Please send the new caption or /cancel to stop. Anything you send now will be set as caption.',
                timeout=300
            )
            if data.text.lower() == '/cancel':
                await data.reply('Cancelled', quote=True)
            else:
                await db.set_caption(data.text.markdown)
                await data.reply('Caption set successfully ✅', quote=True)
        except asyncio.exceptions.TimeoutError:
            await callback_query.answer("Timeout. Try again!", show_alert=True)

    elif query == "add_buttons":
        try:
            data = await client.ask(
                user_id,
                "**Buttons Format:**\n\n"
                "Format: `Text - link`\n\n"
                "For multiple buttons in same row use `|`\n"
                "For multiple rows, use new lines.\n\n"
                "Send buttons or /cancel to stop.",
                timeout=300
            )
            while True:
                if data.text == '/cancel':
                    await data.reply('Cancelled', quote=True)
                    break
                if "-" not in data.text:
                    data = await client.ask(user_id, 'Wrong format! Try again.', timeout=300)
                else:
                    given_buttons = await string_to_buttons(data.text)
                    try:
                        await data.reply('Preview:', reply_markup=InlineKeyboardMarkup(given_buttons))
                        await db.set_buttons(data.text)
                        await data.reply('Buttons set successfully ✅', quote=True)
                        break
                    except ButtonUrlInvalid:
                        data = await client.ask(user_id, 'Invalid URL format! Try again.', timeout=300)
        except asyncio.exceptions.TimeoutError:
            await callback_query.answer("Timeout. Try again!", show_alert=True)

    elif query == "remove_caption":
        await db.set_caption(None)
        await callback_query.answer('Caption removed successfully ✅', show_alert=True)

    elif query == "remove_buttons":
        await db.set_buttons(None)
        await callback_query.answer('Buttons removed successfully ✅', show_alert=True)
    
    elif data == 'chng_req':
        
            try:
                on = off = ""
                if client.REQFSUB:
                    await mdb.set_request_forcesub(False)
                    client.REQFSUB = False
                    off = "🔴"
                    texting = "Disabled ❌"
                else:
                    await mdb.set_request_forcesub(True)
                    client.REQFSUB = True
                    on = "🟢"
                    texting = "Enabled ✅"
        
                button = [
                    [InlineKeyboardButton(f"{on} ON", "chng_req"), InlineKeyboardButton(f"{off} OFF", "chng_req")],
                    [InlineKeyboardButton("Close", "close")]
                ]
                await callback_query.message.edit_text(text=RFSUB_CMD_TXT.format(req_mode=texting), reply_markup=InlineKeyboardMarkup(button)) #🎉)
            except Exception as e:
                print(f"! Error Occured on callback data = 'chng_req' : {e}")


RFSUB_CMD_TXT = """**⚙️ Force Sub Settings**

ForceSub is currently: {req_mode}

Use the buttons below to enable or disable ForceSub.
"""



from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ButtonUrlInvalid
import asyncio.exceptions
from sendbot.db.mdb import mdb
db = mdb
from sendbot.modules.string_buttons import string_to_buttons
from config import ADMIN_ID

@Client.on_message(filters.command("settings") & filters.private & filters.user(ADMIN_ID))
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