import discord
from discord.ext import commands

class General(commands.Cog):
    """General use commands."""

    def __init__(self, client):
        self.client = client

    @commands.command(name='usercount',
                       pass_context=True,
                       description="Output amount of users.")
    async def usercount(self,ctx):
        """Output the amount of users in the server.
        
        Args:
            ctx ([type]): [description]
        """
        await ctx.send(f"```User Count: {len(self.client.users)}```")

    @commands.command(name='oceanman',
                       pass_context=True,
                       description="Listen to the song of our people.")
    async def oceanman(self, ctx):
        """"Listen to the song of our people."""
        await ctx.send(f"{ctx.author.mention} BIG POG! \nhttps://www.youtube.com/watch?v=6E5m_XtCX3c")

    @commands.command(name = 'say', pass_context = True, aliases=["announce"])
    async def say(self,ctx,*,msg):
        """Make bot say what you want.
        Example:
            !say Hello world!
        """
        await ctx.message.delete()
        await ctx.send(msg)
        
def setup(client):
    print("Setting up General Cog...")
    client.add_cog(General(client))
