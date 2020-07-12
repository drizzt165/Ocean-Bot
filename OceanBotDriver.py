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
        """Welcome bot developers and admins to bot-channel upon logging in"""
        if after.guild.id != 102152647489912832: #temp fix to only print in "Ocean Peoples"
            return
        if before.status == after.status:
            return
        
        #bot channel to greet devs/admins
        chanName = 'bot-shit'
        for chan in self.get_all_channels():
            if chan.name == chanName:
                channel = chan
                break    
        channelMembers = channel.members
        if before.status == discord.Status.offline and after.status == discord.Status.online:       
            if after in channelMembers:
                await channel.send(f"Welcome back master {after.mention}")
                
    async def on_message(self, msg):
        #skip for bot messages
        if msg.author == self.user:
            return
        # always have this in on_message or commands won't work
        await self.process_commands(msg)

def setupHelpCommand():
    myHelpCommand = discord.ext.commands.MinimalHelpCommand()
    return myHelpCommand

if __name__ == "__main__":
    tokens = read_token()
    client = Client(command_prefix = ['!'],
                    help_command = setupHelpCommand())
    client.run(tokens['TOKEN'])

