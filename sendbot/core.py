from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton
from config import *
import time, sys
from datetime import datetime
from sendbot.db.mdb import mdb

class app(Client):
    def __init__(self):
        super().__init__(
            name="Adm",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "sendbot/modules"},
            sleep_threshold=15,
        )
        self.START_TIME = time.time()

    async def start(self):
        await super().start()
        bot_info = await self.get_me()
        self.name = bot_info.first_name
        self.username = bot_info.username
        self.uptime = datetime.now()

        self.REQFSUB = await mdb.get_request_forcesub()
        print(self.REQFSUB)
        self.CHANNEL_LIST, self.FSUB_BUTTONS = [], []
        self.REQ_FSUB_BUTTONS = {'normal': [], 'request': {}}
        await self.update_chat_ids()
                
        try:
            db_channel = await self.get_chat(DATABASE_CHANNEL_ID)

            if not db_channel.invite_link:
                db_channel.invite_link = await self.export_chat_invite_link(DATABASE_CHANNEL_ID)

            self.db_channel = db_channel
            
            test = await self.send_message(chat_id=db_channel.id, text="Testing")
            await test.delete()

        except Exception as e:
            print(f"Error: {e}")
            print(f"Make sure the bot is Admin in DB Channel and has proper permissions. Double check the DATABASE_CHANNEL_ID value. Current Value:")
            print("Bot stopped..")
            #sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        print("Bot Started")
        print(f"{self.name} is running!")

        try:
            await self.send_message(ADMIN_ID, text="Bot restarted ♻️")
        except:
            pass

    async def update_chat_ids(self):
        chat_ids = await mdb.get_all_channels()

        if not chat_ids:
            self.CHANNEL_LIST.clear()
            self.FSUB_BUTTONS.clear()
            self.REQ_FSUB_BUTTONS['normal'].clear()
            self.REQ_FSUB_BUTTONS['request'].clear()
            
            return "No Force Subscribe channels found."

        valid_chat_ids, global_buttons, chnl_buttons, req_chnl_buttons = [], [], [], {}
        channel_infos = []

        for chat_id in chat_ids:
            try:
                data = await self.get_chat(chat_id)
                channel_link = data.invite_link 
                channel_name = data.title

                if not channel_link:
                    channel_link = await self.export_chat_invite_link(chat_id)

                temp_butn = [InlineKeyboardButton(text=channel_name, url=channel_link)]

                if not data.username:
                    await mdb.add_reqChannel(chat_id)
                    req_channel_link = await mdb.get_stored_reqLink(chat_id)

                    if not req_channel_link:
                        req_channel_link = (await self.create_chat_invite_link(chat_id=chat_id, creates_join_request=True)).invite_link
                        await mdb.store_reqLink(chat_id, req_channel_link)

                    req_chnl_buttons[chat_id] = [InlineKeyboardButton(text=channel_name, url=req_channel_link)]

                else:
                    chnl_buttons.append(temp_butn)

                global_buttons.append(temp_butn)

                channel_infos.append(f"NAME: {channel_name} (ID: {chat_id})\n")

                valid_chat_ids.append(chat_id)
                    
            except Exception as e:
                print(f"Unable to update {chat_id}, Reason: {e}")
                channel_infos.append(f"ID: {chat_id} - Error occurred: {e}\n")
                continue
        
        invalid_ids = len(chat_ids) - len(valid_chat_ids)

        if invalid_ids:
            channel_infos.append(f"Warning: {invalid_ids} channel IDs may be invalid or bot may not have permissions.\n")

        self.CHANNEL_LIST = valid_chat_ids
        self.FSUB_BUTTONS = global_buttons
        self.REQ_FSUB_BUTTONS['normal'] = chnl_buttons
        self.REQ_FSUB_BUTTONS['request'] = req_chnl_buttons

        return ''.join(channel_infos)

    async def stop(self, *args):
        await super().stop()
        me = await self.get_me()
        print(f"{me.first_name} stopped.")

app = app()
