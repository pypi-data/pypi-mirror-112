from bot import Bot
from intents import Intents
import asyncio
from content import Content

bot = Bot(command_prefix="!*", public_key="05a22e8dbeba245c4180d69d5b49abb3312fc9770958d623de6e6884db58a422", token="Nzg0MTIyMDYxMjE5OTU0NzA4.X8kskw.2PXZhlC0os0xH85Ga1HZ9UMk9MM")
@bot.on()
async def ready():
    print("hi")
@bot.on()
async def message(data):
    if data.author.name == "FrostiiWeeb":
        await data.send("hi master")    
@bot.command()
async def some_basic_command(data):
    await data.send(data.message.channel_id)
   
bot.run()