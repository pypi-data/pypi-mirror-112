import discord, asyncio, aiohttp
from discord.ext import commands
from aioconsole import aprint, ainput
import contextlib, typing
from functools import wraps

__version__ = "0.1.9"

class FancyResponse:
    def __init__(self):
        self.text = ""

class CLI(commands.Bot):
    def __init__(self, channel_id : int, author_id : int = None, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = channel_id
        self.author_id = author_id
        self.cli_start = False
        self.is_using_on_message = False
        
    async def afancy_print(self, text, speed = 0.10, newline=True):
        for letter in text:
            await aprint(letter, end="")
            await asyncio.sleep(speed)
        if newline:
            await aprint("\n", end="")
        response = FancyResponse()
        return response.text

    async def afancy_input(self, text):
        text += " "
        data = await ainput(await self.afancy_print(text, 0.10, newline=False))
        return data
        
        
    async def on_message(self, message):
        await self.wait_until_ready()      
        if self.is_using_on_message:
            pass
        else:
            self.is_using_on_message = True        
        try:
            if self.cli_start is True:
                if message.channel.id == self.channel_id:
                    if message.author == self.user:
                        return
                    if self.author_id:
                        if message.author.id == self.author_id:
                            await self.afancy_print(f"> {message.author} - {message.content}")
                            send_message = await self.afancy_input("[ Admin ] Send a message:")
                            await message.channel.send(send_message)
                    else:
                        await self.afancy_print(f"> {message.author} - {message.content}")
                        send_message = await self.afancy_input("[ Admin ] Send a message:")
                        await message.channel.send(send_message)
        except Exception as e:
            raise commands.CommandInvokeError(e) from e                                     
                    
        await self.process_commands(message)
                
        
    async def start_cli(self):
        cli = await self.afancy_input("Do you want to start the cli? [y | n] (n):")
        cli = cli.lower()
        if cli == "y":
            self.cli_start = True
        elif cli == "n":
            self.cli_start = False
        else:
            await self.afancy_print(f"Invalid Option: {cli}")            
        
    def run(self, token):
        asyncio.get_event_loop().run_until_complete(self.start_cli())
        super().run(token)                                      

class ShardedCLI(CLI, commands.AutoShardedBot):
    pass                                      