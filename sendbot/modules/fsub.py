from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelPrivate
from pyrogram import Client
from pyrogram.types import Message
from sendbot.db.mdb import mdb

INVITE_LINK_CACHE = {}

async def get_fsub(bot: Client, message: Message) -> bool:
    dy = await bot.get_me()
    user_id = message.from_user.id
    not_joined_channels = []
    channels = await mdb.get_all_channels()
    
    for channel_id in channels:
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            if hasattr(bot, 'REQFSUB') and bot.REQFSUB:
                request_exists = await mdb.reqSent_user_exist(channel_id, user_id)
                if request_exists:
                    continue
            
            if channel_id in INVITE_LINK_CACHE:
                chat_title, invite_link = INVITE_LINK_CACHE[channel_id]
            else:
                try:
                    chat = await bot.get_chat(channel_id)
                    chat_title = chat.title
                
                    if hasattr(bot, 'REQFSUB') and bot.REQFSUB:
               
                        invite_link = await bot.create_chat_invite_link(
                            channel_id, 
                            creates_join_request=True
                        )
                        invite_link = invite_link.invite_link
                    else:
    
                        invite_link = chat.invite_link
                        if not invite_link:
                            invite_link = await bot.export_chat_invite_link(channel_id)
                    
                    INVITE_LINK_CACHE[channel_id] = (chat_title, invite_link)
                except (ChatAdminRequired, ChannelPrivate):
                    continue
            
            not_joined_channels.append((chat_title, invite_link))
    
    if not_joined_channels:
        join_buttons = []
        for i in range(0, len(not_joined_channels), 2):
            row = []
            for j in range(2):
                if i + j < len(not_joined_channels):
                    title, link = not_joined_channels[i + j]
                    row.append(InlineKeyboardButton(f"🔔 Join {title}", url=link))
            join_buttons.append(row)
        
        join_buttons.append(
            [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{dy.username}?start=start")]
        )
        
        await message.reply(
            f"👋 {message.from_user.mention}, you need to join my updates channel(s) first.\n\n"
            "Please join and then click **Try Again**.",
            reply_markup=InlineKeyboardMarkup(join_buttons),
        )
        return False
    
    return True
