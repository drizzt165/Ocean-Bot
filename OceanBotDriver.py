import os
import sys
import dotenv
import discord
from discord.ext import commands
import time
import asyncio

class Client(commands.Bot):
    def __init__(self,command_prefix,help_command):
        super().__init__(command_prefix, help_command)
    
    def load_cogs(self,client):
        for cog in [file.split('.')[0] for file in os.listdir("cogs") if file.endswith('.py')]:
            try:
                if cog != "__init__":
                    client.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(e)        
                
    async def on_ready(self):
        print("Loading cogs...")
        self.load_cogs(self)
        print("Bot is ready!")
                
    async def on_message(self, msg):
        #skip for bot messages
        if msg.author == self.user:
            return
        # always have this in on_message or commands won't work
        await self.process_commands(msg)

if __name__ == "__main__":
    client = Client(command_prefix = os.getenv('PREFIX'),
                    help_command = None)
    client.run(os.getenv('TOKEN'))
