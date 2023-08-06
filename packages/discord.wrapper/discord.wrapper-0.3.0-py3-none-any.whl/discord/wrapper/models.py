import datetime, asyncio, aiohttp
from user import User, ClientUser
from guild import Guild

class Author:
    def __init__(self, data={'username': 'FrostiiWeeb', 'public_flags': 128, 'id': '746807014658801704', 'discriminator': '0400', 'avatar': '2ad1c9efba0e94b9a128ef5b7d8a48f4'}):
        self.name = data["username"]
        self.id = int(data["id"])
        self.discriminator = data["discriminator"]
        self.avatar = data["avatar"]
        self.DISCORD_EPOCH = 1420070400000
        self.created_at = self.snowflake_time(self.id)
        
    def __repr__(self):
        return f"<Author name={self.name!r} id={self.id!r} discriminator={self.discriminator!r}>"    
        
    def snowflake_time(self, id: int) -> datetime.datetime:
        timestamp = ((id >> 22) + self.DISCORD_EPOCH) / 1000
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)   
        
class Message:
    def __init__(self, data={"content": "h", "id": 0, "channel_id": 0, "guild_id": 0, "mentions": [], "timestamp": "no"}):
        self.content = data["content"]
        self.id = int(data["id"])
        self.channel_id = int(data["channel_id"])
        self.guild_id = int(data["guild_id"])
        self.mentions = data["mentions"]


    def __repr__(self):
        return f"<Message content={self.content!r} id={self.id!r} mentions={self.mentions!r}>"
        
    def snowflake_time(self, id: int) -> datetime.datetime:
        timestamp = ((id >> 22) + self.DISCORD_EPOCH) / 1000
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)                   

class Data:
    def __init__(self, bot=None, data={'type': 0, 'tts': False, 'timestamp': '2021-05-26T12:13:15.594000+00:00', 'referenced_message': None, 'pinned': False, 'nonce': '853255753656434688', 'mentions': [], 'mention_roles': [], 'mention_everyone': False, 'member': {'roles': [], 'premium_since': None, 'pending': False, 'nick': 'Alex Hutz, the owner of dsc.wrpr', 'mute': False, 'joined_at': '2020-12-24T08:35:46.809000+00:00', 'is_pending': False, 'hoisted_role': None, 'deaf': False, 'avatar': None}, 'id': '847084972803883058', 'flags': 0, 'embeds': [], 'edited_timestamp': None, 'content': 'H', 'components': [], 'channel_id': '381963689470984203', 'author': {'username': 'FrostiiWeeb', 'public_flags': 128, 'id': '746807014658801704', 'discriminator': '0400', 'avatar': '2ad1c9efba0e94b9a128ef5b7d8a48f4'}, 'attachments': [], 'guild_id': '336642139381301249'}):
        self.message = Message(data={"content": data["content"], "timestamp": data["timestamp"], "id": data["id"], "mentions": data["mentions"], "channel_id": data["channel_id"], "guild_id": data["guild_id"]})
        self.author = Author(data["author"])  
        self.bot = bot 
        
    async def send(self, content, embed=None):
        if embed == None:
            return await self.bot.http.post(f"/channels/{self.message.channel_id}/messages", json={"content": str(content)})
        return await self.bot.http.post(f"/channels/{self.message.channel_id}/messages", json=embed)                 