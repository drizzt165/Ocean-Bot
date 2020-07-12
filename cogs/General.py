import discord
from discord.ext import commands

class General(commands.Cog):
    """General use commands."""
    def __init__(self,client):
        self.client = client
        
    @commands.command(name = 'oceanman',
                       pass_context = True,
                       description = "Send link to Ocean Man youtube video.")
    async def say(self,ctx):
        """\nMakes the bot repeat whatever comes after the command."""
        await ctx.send(f"{ctx.author.mention} BIG POG! \nhttps://www.youtube.com/watch?v=6E5m_XtCX3c")
        
def setup(client):
    client.add_cog(General(client))