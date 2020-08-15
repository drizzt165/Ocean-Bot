import os
import dotenv
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, Cog
import mysql.connector


class Admin(commands.Cog):
    """Commands only available to admin users."""
    @has_permissions(administrator = True)
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.red()

    #Check permissions
    async def cog_check(self, ctx):
        validUser = ctx.author.guild_permissions.administrator
        if not validUser:
            embed = discord.Embed(colour = self.EmbedColour)
            commandText = str(ctx.message.content)
            embed.set_author(name = f'You do not have permission to use the command {commandText.split()[0]}')
            embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
            
            await ctx.message.delete()
            await ctx.send(embed = embed)
        
        return validUser

    @commands.command(name = 'test',
                      pass_context = True)
    async def test(self,ctx):
        print(f"{os.getenv('SQLUser')} -> {os.getenv('SQLPass')} -> {os.getenv('SQLHost')}")
        mydb = mysql.connector.connect(
            host = os.getenv('SQLHost'),
            user = os.getenv('SQLUser'),
            passwd = os.getenv('SQLPass'),
            database = 'heroku_2ae506eb86eb6d9'
        )
        guild = ctx.guild
        formattedGuildName = ('_').join([nm.lower() for nm in guild.name.split()])

        myCursor = mydb.cursor()
        
        myCursor.execute("SHOW TABLES")
        tableSet = set()
        for t in myCursor:
            tableSet.add(t[0])

        if formattedGuildName not in tableSet:
            myCursor.execute(f'CREATE TABLE {formattedGuildName} (channelName VARCHAR(50), messageCount INTEGER, date VARCHAR(15))')

        sqlStuff = f"INSERT INTO {formattedGuildName} (channelName, messageCount, date) VALUES (%s, %s, %s)"
        record = (ctx.channel.name, 15, datetime.date(datetime.now()))

        myCursor.execute(sqlStuff, record)
        mydb.commit()

    @commands.command(name = 'msg_count',
                       pass_context = True,
                       description = "Print amount of messages in a channel.")
    async def msg_count(self,ctx,channel:discord.TextChannel = None):
        embed = discord.Embed(colour = self.EmbedColour)

        channel = channel or ctx.channel
        count = 0
        async for _ in channel.history(limit=None):
            count += 1

        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        embed.add_field(name = f'Message count:', value = f'{count} messages in {channel.mention}')

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name = 'msg_graph',
                      pass_context = True,
                      description = "Print graph of message history.")
    async def msg_graph(self,ctx):
        embed = discord.Embed(colour = self.EmbedColour)

        guild = ctx.guild
        textChannels = guild.text_channels
        
        for c in textChannels:
            count = 0
            async for _ in c.history(limit=None):
                count+=1
            embed.add_field(name = f'Message count for #{c.name}', value = count, inline = False)

        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        
        await ctx.message.delete()
        await ctx.send(embed=embed)

def setup(client):
    print("Setting up Admin Cog...")
    client.add_cog(Admin(client))
    