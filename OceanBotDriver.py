import os
import json
import discord
from discord.ext import commands
import time
import asyncio

def read_token():
    with open("settings/tokens.json") as tok:
        return json.load(tok)

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
        
    async def on_member_update(self, before, after):
        if before.status == after.status:
            return
        if before.status == discord.Status.offline and after.status == discord.Status.online:
            nameList = ['drizzt165']
            if str(after.name) in nameList:
                print(after.joined_at)

def setupHelpCommand():
    myHelpCommand = discord.ext.commands.MinimalHelpCommand()
    return myHelpCommand
         
    #test code
    # async def on_message(self,msg):
    #     print(msg.author.mention)

if __name__ == "__main__":
    tokens = read_token()
    client = Client(command_prefix = ['!'],
                    help_command = setupHelpCommand())
    client.run(tokens['TOKEN'])
