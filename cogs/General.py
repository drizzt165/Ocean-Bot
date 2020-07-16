import discord
from discord.ext import commands

class General(commands.Cog):
    """General use commands."""

    def __init__(self, client):
        self.client = client

    @commands.command(name = 'user',
                      pass_context = True,
                      description = "Output stats of mentioned member.")
    async def user(self,ctx):
        """Make bot output user stats.

        Args:
            ctx ([type]): [description]
            msg ([type]): [description]
        """
        target = ctx.message.mentions[0]
        joinDiscDate = str(target.created_at).split(' ')[0]
        joinServDate = str(target.joined_at).split(' ')[0]
        
        print(joinDiscDate)
        output = f"```ID: {target.name}#{target.discriminator}\n"\
                       f"Nickname: {target.nick}\n"\
                       f"Joined Discord: {joinDiscDate}\n"\
                       f"Joined Server: {joinServDate}\n\n"\
                       f"Current activity: {target.activities}\n```"
        await ctx.send(output)
        
    @commands.command(name='usercount',
                       pass_context=True,
                       description="Output amount of users.")
    async def usercount(self,ctx):
        """Output the amount of users in the server.
        
        Args:
            ctx ([type]): [description]
        """
        guild = ctx.author.guild
        totalMembers = guild.member_count
        onlineMembers = 0
        offlineMembers = 0
        idleMembers = 0
        dndMembers = 0
        for mem in guild.members:
            memStatus = mem.status
            if memStatus == discord.Status.online:
                onlineMembers+=1
            elif memStatus == discord.Status.offline:
                offlineMembers+=1
            elif memStatus == discord.Status.idle:
                idleMembers += 1
            elif memStatus == discord.Status.dnd:
                dndMembers += 1
            
        await ctx.send(f"```User Count: {totalMembers}\n"\
                       f"Online: {onlineMembers}\n"\
                       f"Offline: {offlineMembers}\n"\
                       f"Idle: {idleMembers}\n"\
                       f"DND: {dndMembers}```\n")

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
