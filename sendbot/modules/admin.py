
from pyrogram import Client, filters
from pyrogram.types import *
from sendbot.db.udb import udb
from sendbot.db.mdb import mdb
from config import ADMIN_ID
import asyncio
from pyrogram.errors import *

@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN_ID))
async def broadcasting_func(client: Client, message: Message):
    try:
        msg = await message.reply_text("Wait a second!")
        if not message.reply_to_message:
            return await msg.edit("<b>Please reply to a message to broadcast.</b>")
        await msg.edit("Processing ...")
        completed = 0
        failed = 0
        to_copy_msg = message.reply_to_message
        users_list = await udb.get_all_users()

        for i, userDoc in enumerate(users_list):
            if i % 20 == 0:
                await msg.edit(f"Total: {i}\nCompleted: {completed}\nFailed: {failed}")
            user_id = userDoc.get("user_id")
            if not user_id:
                continue
            try:
                await to_copy_msg.copy(int(user_id))
                completed += 1
                await asyncio.sleep(0.1)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await to_copy_msg.copy(int(user_id))
                    completed += 1
                except Exception:
                    failed += 1
            except Exception as e:
                print(f"Error in broadcasting to {user_id}: {e}")
                failed += 1

        await msg.edit(f"Successfully Broadcasted\nTotal: {len(users_list)}\nCompleted: {completed}\nFailed: {failed}")
    except Exception as e:
        print(f"Error in broadcast: {e}")
        await message.reply_text("An error occurred while broadcasting.")

@Client.on_message(filters.command("ban") & filters.private & filters.user(ADMIN_ID))
async def ban_user_cmd(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Usage: /ban user_id")
            return
        user_id = int(command_parts[1])
        reason = " ".join(command_parts[2:]) if len(command_parts) > 2 else None
        try:
            user = await client.get_users(user_id)
        except Exception:
            await message.reply_text("Unable to find user.")
            return
        if await udb.ban_user(user_id, reason):
            ban_message = f"User {user.mention} has been banned."
            if reason:
                ban_message += f"\nReason: {reason}"
            await message.reply_text(ban_message)
        else:
            await message.reply_text("Failed to ban user.")
    except ValueError:
        await message.reply_text("Please provide a valid user ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("maintenance") & filters.private & filters.user(ADMIN_ID))
async def maintenance_mode(client: Client, message: Message):
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text("Usage: /maintenance [on/off]")
            return

        status = args[1].lower()
        if status not in ["on", "off"]:
            await message.reply_text("Invalid status. Use 'on' or 'off'")
            return

        await mdb.set_maintenance_status(status == "on")
        await message.reply_text(f"Maintenance mode {'activated' if status == 'on' else 'deactivated'}")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")


@Client.on_message(filters.command("unban") & filters.private & filters.user(ADMIN_ID))
async def unban_user_cmd(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply_text("Usage: /unban user_id")
            return
        user_id = int(command_parts[1])
        try:
            user = await client.get_users(user_id)
        except Exception:
            await message.reply_text("Unable to find user.")
            return
        if await udb.unban_user(user_id):
            await message.reply_text(f"User {user.mention} has been unbanned.")
        else:
            await message.reply_text("Failed to unban user or user was not banned.")
    except ValueError:
        await message.reply_text("Please provide a valid user ID.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("deleteall") & filters.private & filters.user(ADMIN_ID))
async def delete_all_videos_command(client, message):
    try:
        t = await message.reply_text("**Proceed to delete all videos ♻️**")
        await mdb.delete_all_videos()
        await t.edit_text("**All videos have been deleted from the database**")
    except Exception as e:
        await message.reply_text(f"**Error: {str(e)}*")

@Client.on_message(filters.command("delete") & filters.private & filters.user(ADMIN_ID))
async def delete_video_by_id_command(client, message):
    if len(message.command) < 2:return
    await message.reply_text("Please provide a video ID to delete.")
    video_id = int(message.command[1])
    deleted = await mdb.delete_video_by_id(video_id)
    if deleted:
        await message.reply_text(f"Deleted video with ID `{video_id}`")
    else:
        await message.reply_text(f"⚠️ Video ID `{video_id}` not found.")
