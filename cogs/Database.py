import dotenv
import discord
from datetime import datetime
from discord.ext import commands

class Database(commands.Cog):
    """Commands to interact with the SQL database."""
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.blue()

    @commands.command(name = 'msgCount',
                      pass_context = True,
                      description = 'Show message count of current channel. Only counts user messages, not bots.')
    async def msgCount(self,ctx):
        embed = discord.Embed(colour = self.EmbedColour)
        msgCount = await self.client.dbManager.get_channelMsgCount(ctx)
        embed.add_field(
            name = f"Message count for #{ctx.channel.name}",
            value = f"{msgCount}"
            )
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed = embed)
        
def setup(client):
    print("Setting up Database Cog...")
    client.add_cog(Database(client))