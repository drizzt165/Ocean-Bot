import os
import sys
import dotenv
import discord
from discord.ext import commands
import time
import asyncio
from customPackages import dbManager as db
from mysql.connector import errors as SQLError
from enum import Enum


class dbState(Enum):
    INITIALIZING = 1
    RECONNECTING = 2
    UPDATING = 3
    FREE = 4


class Client(commands.Bot):
    def __init__(self,command_prefix,help_command):
        super().__init__(command_prefix, help_command)
        self.EmbedColour = discord.Colour.blurple()

        #manage messages while database is initializing and counting past messages (can take some time)
        self.dbState = dbState.FREE
        self.msgBuffer = []

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
        try:
            await self.dbManager.removeServer(guild)
        except SQLError.ProgrammingError as e:
            pass

    async def on_guild_join(self,guild):
        embed = discord.Embed(colour = self.EmbedColour)
        embed.add_field(name = 'Initializing Bot resources: ', value =  'This may take a few minutes depending on server size and age, please wait...')

        tempMsg = await guild.text_channels[0].send(embed = embed)
        try:
            self.dbState = dbState.INITIALIZING
            await self.dbManager.init_Server(guild)
        except SQLError.ProgrammingError as e:
            self.dbState = dbState.INITIALIZING
            await self.dbManager.init_table()
            await self.dbManager.init_Server(guild)
        except SQLError.OperationalError as e:
            self.dbState = dbState.RECONNECTING
            print('Reconnecting to database')
            self.dbManager = db.dbManager(os.getenv('SQLHost'),os.getenv('SQLUser'),os.getenv('SQLPass'),os.getenv('DATABASE'))
            try:
                self.dbState = dbState.INITIALIZING
                await self.dbManager.init_Server(guild)
            except SQLError.ProgrammingError as e:
                self.dbState = dbState.INITIALIZING
                await self.dbManager.init_table()
                await self.dbManager.init_Server(guild)

        self.dbState = dbState.FREE
        await tempMsg.delete()

    async def on_guild_channel_delete(self,channel):
        self.dbManager.removeChannel(channel)

    async def on_guild_channel_create(self,channel):
        self.dbManager.addChannel(channel)

    async def on_message_delete(self,msg):
        await self.dbManager.updateDB(msg,-1)

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            embed = discord.Embed(colour = self.EmbedColour)
            embed.add_field(name = f"Command '{context.message.content}'' does not exist.", value = 'Use the !help command to see available commands.')
            await context.send(embed = embed)
        else:
            raise exception

    async def on_message(self, msg):
        if msg.author.bot:
            return
        async with msg.channel.typing():
            #increment msg count or initialize the database if the table/row doesn't exist
            if self.dbState == dbState.FREE:
                try:
                    self.dbState = dbState.UPDATING
                    await self.dbManager.updateDB(msg)
                except (SQLError.ProgrammingError, TypeError) as e:
                    try:
                        self.dbState = dbState.INITIALIZING
                        print("Initializing database first.")
                        await self.dbManager.init_table()
                        await self.dbManager.init_Server(msg.guild)

                # Would like a more elegant solution here if possible.
                # Don't like pasting this code for the same exception just different code.
                    except SQLError.OperationalError as e:
                        self.dbState = dbState.RECONNECTING
                        print('Reconnecting to database')
                        self.dbManager = db.dbManager(os.getenv('SQLHost'),os.getenv('SQLUser'),os.getenv('SQLPass'),os.getenv('DATABASE'))
                except SQLError.OperationalError as e:
                    self.dbState = dbState.RECONNECTING
                    print('Reconnecting to database')
                    self.dbManager = db.dbManager(os.getenv('SQLHost'),os.getenv('SQLUser'),os.getenv('SQLPass'),os.getenv('DATABASE'))
            else:
                self.msgBuffer.append(msg)
                return

            self.dbState = dbState.FREE

            # always have this in on_message or commands won't work
            await self.process_commands(msg)

            # process any commands requested while database code was busy
            if self.msgBuffer:
                for _ in range(len(self.msgBuffer)):
                    await self.process_commands(self.msgBuffer.pop(0))

if __name__ == "__main__":
    client = Client(command_prefix = os.getenv('PREFIX'),
                    help_command=None)
    client.run(os.getenv('TOKEN'))
