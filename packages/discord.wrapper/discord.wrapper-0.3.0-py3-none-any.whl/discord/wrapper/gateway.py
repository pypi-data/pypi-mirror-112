import json
import asyncio, functools
import aiohttp
import json
from user import User, ClientUser
from guild import Guild
from string import Template
from io import StringIO
import ast
from models import Data
import asyncio
import functools
import traceback
from models import Data
	                
class Gateway:
	def __init__(self, bot):
		self.bot = bot 
	
	async def get_data(self):
		   data = await self.ws.receive()
		   return data.data					  
			
	def identify_json(self, token : str, intents : int):
		"""
		The identify payload to authorize the bot.
		
		Attributes
		----------
		
		token : str
			The token of the bot.
		intents : int
			The intents for the bot.
		"""
		
		t = Template('{"op": 2,"d": {"token": "$token","intents": $intents, "properties": {"$os": "linux","$browser": "discord.wrapper","$device": "discord.wrapper"}, "status": "dnd", "since": 91879201, "afk": false},"s": null,"t": null}')
		t = t.substitute(token=str(token), intents=intents, os="$os", browser="$browser", device="$device")

		return t
	
	
	async def close(self):
		"""
		The |async| function to close the connection.
		"""
				
		await self.ws.close()		    		
		
	async def start(self, _token : str, _intents : int):
		"""
		Function to connect the bot to discord.
		
		Attributes
		----------
		
		_token : str
			The token of the bot.
		_intents : int
			The intents for the bot.
		"""		
		try:
			self.ws = await aiohttp.ClientSession().ws_connect("wss://gateway.discord.gg/?v=6&encoding=json") 
			async for msg in self.ws:
			    dataa = json.loads(msg.data)			   
			    if dataa['op'] == 10:
			        
			        heartbeat = '{"op": 1,"d": 251}'
			        p = self.identify_json(_token, _intents)
			        p_j= json.loads(p)
			        h_j = json.loads(heartbeat)
			        await self.ws.send_json(h_j)		
			        await self.ws.send_json(p_j)
			    elif dataa["op"] == 11:
			        pass
			    elif dataa["op"] == 0:
			        if dataa["t"] == "READY":
			            for event, func in self.bot.listeners:
			                if event == "ready":
			                    await func()	
			        if dataa["t"] == "MESSAGE_CREATE":
			            for event, func in self.bot.listeners:
			                if event == "message":
			                    await func(data=Data(bot=self.bot, data=dataa["d"]))                           
			        if dataa["t"] == "MESSAGE_CREATE":			            			            			        
			            for command, func in self.bot.commands:
			                if dataa["d"]["content"] == f"{self.bot.command_prefix}{command}":			                    
			                    await func(data=Data(bot=self.bot, data=dataa["d"]))	          
			        if dataa["t"] == "INTERACTION_CREATE":
			            for cmd, func in self.bot.slash_commands:
			                if   
			    else:
			        print(data)				
		except Exception as e:
		    print("InvokeError: ")
		    traceback.print_exc()
	
	def connect(self, token : str, intents : int):
		"""
		The actual function to connect the bot to discord.
		
		Attributes
		----------
		
		token : str
			The token of the bot.
		intents : int
			The intents for the bot.
		"""		
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		asyncio.ensure_future(self.start(token, intents), loop=loop)
		loop.run_forever()																					
