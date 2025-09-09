from sendbot import app
import asyncio
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMIN_ID
from pyrogram import Client, filters
from sendbot.db.mdb import mdb


@app.on_message(filters.command('add_fsub') & filters.private & filters.user(ADMIN_ID))
async def add_forcesub(client: Client, message: Message):
    pro = await message.reply("Processing...", quote=True)
    check = 0
    channel_ids = await mdb.get_all_channels()
    fsubs = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close ✖️", callback_data="close")]])
    
    if not fsubs:
        await pro.edit(
            "You need to provide channel IDs.\n\nExample:\n"
            "/add_fsub [channel_ids]\n\n"
            "You can add one or multiple channel IDs at a time.",
            reply_markup=reply_markup
        )
        return

    channel_list = ""
    for id in fsubs:
        try:
            id = int(id)
        except:
            channel_list += f"Invalid ID: <code>{id}</code>\n\n"
            continue
            
        if id in channel_ids:
            channel_list += f"ID: <code>{id}</code> already exists.\n\n"
            continue
            
        id = str(id)
        if id.startswith('-') and id[1:].isdigit() and len(id) == 14:
            try:
                data = await client.get_chat(id)
                link = data.invite_link
                cname = data.title

                if not link:
                    link = await client.export_chat_invite_link(id)
                    
                channel_list += f"Name: <a href={link}>{cname}</a> (ID: <code>{id}</code>)\n\n"
                check += 1
                
            except Exception as e:
                print(f'Error occured on decode, reason: {e}')
                channel_list += f"ID: <code>{id}</code>\nUnable to add force-sub. Please check the channel ID or bot permissions.\n\n"
            
        else:
            channel_list += f"Invalid ID: <code>{id}</code>\n\n"
            continue
    
    if check == len(fsubs):
        for id in fsubs:
            await mdb.add_channel(int(id))

        await pro.edit('Updating channel ID list...')
        await client.update_chat_ids()

        await pro.edit(
            f'Force-Sub Channels Added ✅\n\n{channel_list}',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        
    else:
        await pro.edit(
            f'❌ Error occurred while adding Force-Sub Channels.\n\n{channel_list.strip()}\n\n'
            'Please try again.',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )


@app.on_message(filters.command('del_fsub') & filters.private & filters.user(ADMIN_ID))
async def delete_all_forcesub(client: Client, message: Message):
    pro = await message.reply("Processing...", quote=True)
    channels = await mdb.get_all_channels()
    fsubs = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close ✖️", callback_data="close")]])

    if not fsubs:
        return await pro.edit(
            "Please provide valid IDs or arguments.\n\nExamples:\n"
            "/del_fsub [channel_ids] - delete one or more specific IDs\n"
            "/del_fsub all - delete all Force-Sub IDs",
            reply_markup=reply_markup
        )

    if len(fsubs) == 1 and fsubs[0].lower() == "all":
        if channels:
            for id in channels:
                await mdb.del_channel(id)
                    
            ids = "\n".join(f"<code>{channel}</code> ✅" for channel in channels)

            await pro.edit('Updating channel ID list...')
            await client.update_chat_ids()

            return await pro.edit(f"All Force-Sub channel IDs have been deleted:\n{ids}", reply_markup=reply_markup)
        else:
            return await pro.edit("No channel IDs available to delete.", reply_markup=reply_markup)
            
    if len(channels) >= 1:
        passed = ''
        for sub_id in fsubs:
            try:
                id = int(sub_id)
            except:
                passed += f"Invalid ID: <code>{sub_id}</code>\n"
                continue
            if id in channels:
                await mdb.del_channel(id)
                passed += f"<code>{id}</code> ✅\n"
            else:
                passed += f"<code>{id}</code> is not in Force-Sub channels.\n"
        
        await pro.edit('Updating channel ID list...')
        await client.update_chat_ids()
                
        await pro.edit(f"The provided channel IDs have been deleted:\n\n{passed}", reply_markup=reply_markup)
        
    else:
        await pro.edit("No channel IDs available to delete.", reply_markup=reply_markup)
      

@app.on_message(filters.command('fsub_chnl') & filters.private & filters.user(ADMIN_ID))
async def get_forcesub(client: Client, message: Message):
    pro = await message.reply('Fetching channel ID list...', quote=True)
    await message.reply_chat_action(ChatAction.TYPING)

    channel_list = await client.update_chat_ids()
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Close ✖️", callback_data="close")]])
    await message.reply_chat_action(ChatAction.CANCEL)

    await pro.edit(
        f"Force-Sub Channel List:\n\n{channel_list}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
