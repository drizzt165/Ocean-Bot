import discord
from discord.ext import commands

class Admin(commands.Cog):
    """Admin use commands."""
    def __init__(self,client):
        self.client = client
        
    @commands.command(name = 'say', pass_context = True, aliases=["announce"])
    async def say(self,ctx,*,msg):
        """Make bot say what you want.
        Example:
            !say Hello world!
        """
        await ctx.message.delete()
        await ctx.send(msg)
    
def setup(client):
    client.add_cog(Admin(client))
    