from bot import Bot
from intents import Intents
import asyncio

bot = Bot(token="NzEwMjEzMzkwMzc4ODYwNTg2.XrxLww.3cvKarFHT9iaBprIteq14-AW0fo", intents=513, public_key="c94e9f26734665c4fac00a5d73dc5ed848ba98800e5d66f4c3b4b41b51934fb1", command_prefix="bp.")
@bot.on()
async def ready():
    print("READY!")
@bot.command()
async def hi(data):
    await data.send("Hello!")               
bot.run()