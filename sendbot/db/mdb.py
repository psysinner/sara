from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
from datetime import datetime, timedelta
import asyncio
from itertools import count

from itertools import count
from zoneinfo import ZoneInfo

class Database:
    def __init__(self):
        self.last_reset_time = datetime.now()
        self.async_client = AsyncIOMotorClient(MONGO_URI)
        self.async_db = self.async_client["adultzonebot"]
        self.async_video_collection = self.async_db["videos"]
        self.async_user_collection = self.async_db["users"]
        self.async_limits_collection = self.async_db["limits"]
        self.async_global_limits = self.async_db["global_limits"]

        self.channel_data = self.async_db['channels']
        self.rqst_fsub_data = self.async_db['request_forcesub']
        self.rqst_fsub_Channel_data = self.async_db['request_forcesub_channel']
        self.store_reqLink_data = self.async_db['store_reqLink']

        self.msginfo = self.async_db['msginfo']

        


    async def get_global_limits(self):
        default_limits = {
            'free_limit': 10,
            'prime_limit': 50,
            'maintenance': False
        }
        db_limits = await self.async_global_limits.find_one({}) or {}
        return {**default_limits, **db_limits}

    async def initialize_global_limits(self):
        if not await self.async_global_limits.find_one({}):
            await self.async_global_limits.insert_one({
                'free_limit': 10,
                'prime_limit': 50,
                'maintenance': False
            })

    async def update_global_limits(self, free_limit: int, prime_limit: int):
        await self.async_limits_collection.update_one(
            {"_id": "global_limits"},
            {"$set": {"free_limit": free_limit, "prime_limit": prime_limit}},
            upsert=True
        )

    async def increment_daily_count(self, user_id: int):
        user = await self.get_user(user_id)
        today = datetime.now()
        if user.get("last_request_date") is None or user.get("last_request_date").date() != today.date():
            await self.update_user(user_id, {"daily_count": 1, "last_request_date": today})
            return 1
        else:
            new_count = user.get("daily_count", 0) + 1
            await self.update_user(user_id, {"daily_count": new_count})
            return new_count
        
    async def update_global_limit(self, limit_type, new_value):
        if limit_type == "free":
            await self.async_user_collection.update_many({"plan": "free"}, {"$set": {"daily_limit": new_value}})
            await self.async_limits_collection.update_one(
                {"_id": "global_limits"},
                {"$set": {"free_limit": new_value}},
                upsert=False
            )
            await self.async_global_limits.update_one(
                {},
                {"$set": {"free_limit": new_value}},
                upsert=False
            )
        elif limit_type == "prime":
            await self.async_user_collection.update_many({"plan": "prime"}, {"$set": {"daily_limit": new_value}})
            await self.async_limits_collection.update_one(
                {"_id": "global_limits"},
                {"$set": {"prime_limit": new_value}},
                upsert=False
            )
            await self.async_global_limits.update_one(
                {},
                {"$set": {"prime_limit": new_value}},
                upsert=False
            )
        return True



    async def set_maintenance_status(self, status: bool):
        await self.async_global_limits.update_one(
            {},
            {'$set': {'maintenance': status}},
            upsert=True
        )
        limits = await self.async_limits_collection.find_one({"_id": "global_limits"})
        if not limits:
            default_limits = {
                "_id": "global_limits",
                "free_limit": 10,
                "prime_limit": 50
            }
            await self.async_limits_collection.insert_one(default_limits)
            return default_limits
        return limits
        


            
    async def get_all_premium_users(self):
        cursor = self.async_user_collection.find({"plan": 'prime'})
        return [doc async for doc in cursor]
        
    async def add_prime(self, user_id: int, duration_str: str):
        try:
            parts = duration_str.split()
            if len(parts) != 2 or parts[1] not in ("s", "m", "h", "d", "y"):
                return False
            amount = int(parts[0])
            unit = parts[1]
            if amount <= 0:
                return False
            now = datetime.now()
            expiry_date = now
            if unit == 's':
                expiry_date += timedelta(seconds=amount)
            elif unit == 'm':
                expiry_date += timedelta(minutes=amount)
            elif unit == 'h':
                expiry_date += timedelta(hours=amount)
            elif unit == 'd':
                expiry_date += timedelta(days=amount)
            elif unit == 'y':
                expiry_date += timedelta(days=amount*365)
            expiry_date = expiry_date.replace(second=0, microsecond=0)
            limits = await self.get_global_limits()
            user = await self.get_user(user_id)
            if user.get('plan') == 'prime':
                await self.remove_premium(user_id)
                user = await self.get_user(user_id)
            current_daily_count = user.get('daily_count', 0)
            current_last_request = user.get('last_request_date', now)
            result = await self.async_user_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "plan": "prime",
                        "daily_limit": limits["prime_limit"],
                        "daily_count": current_daily_count,
                        "prime_expiry": expiry_date,
                        "last_request_date": current_last_request,
                        "remaining_time": format_remaining_time(expiry_date)
                    }
                }
            )
            if result.modified_count > 0:
                updated_user = await self.get_user(user_id)
                return updated_user.get("plan") == "prime"
            return False
        except ValueError as e:
            print(f"Error in add_prime: {e}")
            return False

    async def remove_premium(self, user_id: int):
        limits = await self.get_global_limits()
        await self.async_user_collection.update_one(
            {"_id": user_id},
            {"$set": {
                "plan": "free",
                "daily_limit": limits["free_limit"],
                "has_premium": False
            },
            "$unset": {
                "prime_expiry": "",
                "remaining_time": "",
                "premium_expire": ""
            }}
        )



    async def save_video_id(self, video_id: int, duration: int, is_premium: bool = False):
        video_data = {
            "video_id": video_id,
            "duration": duration,
            "is_premium": is_premium,
            "added_at": datetime.now()
        }
        if not await self.async_video_collection.find_one({"video_id": video_id}):
            await self.async_video_collection.insert_one(video_data)

    async def get_all_videos(self):
        videos = []
        async for video in self.async_video_collection.find({}):
            videos.append(video)
        return videos
    
    async def count_all_videos(self):
        return await self.async_video_collection.count_documents({})

    async def get_free_videos(self):
        videos = []
        async for video in self.async_video_collection.find({"is_premium": False}):
            videos.append(video)
        return videos

    async def get_user(self, user_id: int):
        user = await self.async_user_collection.find_one({"_id": user_id})
        if not user:
            limits = await self.get_global_limits()
            default_user = {
                "_id": user_id,
                "plan": "free",
                "daily_count": 0,
                "daily_limit": limits["free_limit"],
                "last_request_date": datetime.now(),
                "sent_videos": [],
                "prime_expiry": None,
                "remaining_time": None
            }
            await self.async_user_collection.insert_one(default_user)
            return default_user
        return user

    async def update_user(self, user_id: int, update_data: dict):
        await self.async_user_collection.update_one({"_id": user_id}, {"$set": update_data})

    async def get_sent_videos(self, user_id: int):
        user_data = await self.async_user_collection.find_one({"_id": user_id})
        return user_data.get("sent_videos", []) if user_data else []
        
    async def is_message_sent_to_user(self, user_id: int, message_id: int):
        user_data = await self.get_user(user_id)
        sent_videos = user_data.get("sent_videos", [])
        if not isinstance(sent_videos, list):
            sent_videos = []
        return any(entry.get("message_id") == message_id for entry in sent_videos if isinstance(entry, dict))




    async def remove_sent_video(self, user_id: int, video_id: int):
        await self.async_user_collection.update_one(
            {"_id": user_id},
            {"$pull": {"sent_videos": {"video_id": video_id}}}
        )
    async def delete_all_videos(self):
        await self.async_video_collection.delete_many({})

    async def delete_video_by_id(self, video_id: int):
        await self.async_video_collection.delete_one({"video_id": video_id})
        return True

    async def add_reqChannel(self, channel_id: int):
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$setOnInsert': {'user_ids': []}},  
            upsert=True 
        )


    async def reqSent_user(self, channel_id: int, user_id: int):
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$addToSet': {'user_ids': user_id}}, 
            upsert=True
        )

    async def del_reqSent_user(self, channel_id: int, user_id: int):
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$pull': {'user_ids': user_id}}
        )
        
    async def clear_reqSent_user(self, channel_id: int):
        if await self.reqChannel_exist(channel_id):
            await self.rqst_fsub_Channel_data.update_one(
                {'_id': channel_id}, 
                {'$set': {'user_ids': []}}
            )

    async def reqSent_user_exist(self, channel_id: int, user_id: int):
        found = await self.rqst_fsub_Channel_data.find_one(
            {'_id': channel_id, 'user_ids': user_id}
        )
        return bool(found)

    async def del_reqChannel(self, channel_id: int):
        await self.rqst_fsub_Channel_data.delete_one({'_id': channel_id})

    async def reqChannel_exist(self, channel_id: int):
        found = await self.rqst_fsub_Channel_data.find_one({'_id': channel_id})
        return bool(found)

    async def get_reqSent_user(self, channel_id: int):
        data = await self.rqst_fsub_Channel_data.find_one({'_id': channel_id})
        if data:
            return data.get('user_ids', [])
        return []

    async def get_reqChannel(self):
        channel_docs = await self.rqst_fsub_Channel_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    async def channel_exist(self, channel_id: int):
        found = await self.channel_data.find_one({'_id': channel_id})
        return bool(found)
        
    async def add_channel(self, channel_id: int):
        if not await self.channel_exist(channel_id):
            await self.channel_data.insert_one({'_id': channel_id})
            return
    
    async def del_channel(self, channel_id: int):
        if await self.channel_exist(channel_id):
            await self.channel_data.delete_one({'_id': channel_id})
            return
    
    async def get_all_channels(self):
        channel_docs = await self.channel_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    async def get_request_forcesub(self):
        data = await self.rqst_fsub_data.find_one({})
        if data:
            return data.get('value', False)
        return False
    async def get_admin_state(self, user_id):
        user = await self.async_user_collection.find_one({'_id': user_id})
        return user.get('admin_state') if user else None
    async def get_reqChannel(self):
        channel_docs = await self.rqst_fsub_Channel_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids
        
    async def get_reqLink_channels(self):
        channel_docs = await self.store_reqLink_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    async def get_stored_reqLink(self, channel_id: int):
        data = await self.store_reqLink_data.find_one({'_id': channel_id})
        if data:
            return data.get('link')
        return None

    async def store_reqLink(self, channel_id: int, link: str):
        await self.store_reqLink_data.update_one(
            {'_id': channel_id}, 
            {'$set': {'link': link}}, 
            upsert=True
        )

    async def del_stored_reqLink(self, channel_id: int):
        await self.store_reqLink_data.delete_one({'_id': channel_id})
    
    async def set_caption(self, caption):
        result = await self.msginfo.update_one(
            {'id': '0'}, 
            {'$set': {'caption': caption}}, 
            upsert=True
        )
        return result.modified_count > 0
        
    async def get_caption(self):
        channel = await self.msginfo.find_one({'id': '0'})
        return channel['caption'] if channel and channel.get('caption') else ''

    async def set_buttons(self, buttons):
        result = await self.msginfo.update_one(
            {'id': '0'}, 
            {'$set': {'buttons': buttons}}, 
            upsert=True
        )
        return result.modified_count > 0
        
    async def get_buttons(self):
        channel = await self.msginfo.find_one({'id': '0'})
        return channel['buttons'] if channel and channel.get('buttons') else None
    
    async def set_request_forcesub(self, value: bool):
        existing = await self.rqst_fsub_data.find_one({})
        if existing:
            await self.rqst_fsub_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.rqst_fsub_data.insert_one({'value': value})


def format_remaining_time(expiry):
    delta = expiry - datetime.now()
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

mdb = Database()
