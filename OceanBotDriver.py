import os
import sys
import dotenv
import discord
from discord.ext import commands
import time
import asyncio
from customPackages import dbManager as db
from mysql.connector import errors as SQLError

class Client(commands.Bot):
    def __init__(self,command_prefix,help_command):
        super().__init__(command_prefix, help_command)

        #connect to database
        self.dbManager = db.dbManager(os.getenv('SQLHost'),os.getenv('SQLUser'),os.getenv('SQLPass'),os.getenv('DATABASE'))
    
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
        await client.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(type=discord.ActivityType.watching, name="for !help"))
        print("Bot is ready!")

    async def on_guild_remove(self,guild):
        await self.dbManager.removeServer(guild)

    async def on_guild_join(self,guild):
        await self.dbManager.addServer(guild)

    async def on_guild_channel_delete(self,channel):
        self.dbManager.removeChannel(channel)

    async def on_guild_channel_create(self,channel):
        self.dbManager.addChannel(channel)

    async def on_message_delete(self,msg):
        await self.dbManager.updateDB(msg,-1)

    async def on_message(self, msg):
        if msg.author.bot:
            return
        
        #increment msg count or initialize the database if the table/row doesn't exist
        try:
            await self.dbManager.updateDB(msg)
        except (SQLError.ProgrammingError, TypeError) as e:
            try:
                print("Initializing database first.")
                await self.dbManager.init_table(msg)
                await self.dbManager.init_rows(msg)

        # Would like a more elegant solution here if possible.
        # Don't like pasting this code for the same exception just different code.
            except SQLError.OperationalError as e:
                print('Reconnecting to database')
                self.dbManager = db.dbManager(os.getenv('SQLHost'),os.getenv('SQLUser'),os.getenv('SQLPass'),os.getenv('DATABASE'))
        except SQLError.OperationalError as e:
            print('Reconnecting to database')
            self.dbManager = db.dbManager(os.getenv('SQLHost'),os.getenv('SQLUser'),os.getenv('SQLPass'),os.getenv('DATABASE'))
        
        # always have this in on_message or commands won't work
        await self.process_commands(msg)


if __name__ == "__main__":
    client = Client(command_prefix = os.getenv('PREFIX'),
                    help_command=None)
    client.run(os.getenv('TOKEN'))
