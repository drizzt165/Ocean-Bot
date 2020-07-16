import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name = 'help',
                      pass_context = True,
                      description = "Print list of commands.")
    async def help(self,ctx,*,msg = None):
        embed = discord.Embed(
            colour = discord.Colour.orange()
        )
        
        embed.set_author(name = 'Ocean-Bot Commands')
        commands = [command for command in self.client.commands 
                    if command.name != 'help' and
                    command.description and
                    command.name]
        
        for command in commands:
            embed.add_field(name = command.name,
                            value = command.description,
                            inline = False)
  
        await ctx.send(embed=embed)        
        
    @commands.command(name = 'user',
                      pass_context = True,
                      description = "Output stats of mentioned member.")
    async def user(self,ctx):
        target = ctx.message.mentions[0]
        joinDiscDate = str(target.created_at).split(' ')[0]
        joinServDate = str(target.joined_at).split(' ')[0]

        embed = discord.Embed()
        
        embed.set_author(name=f"{target}", 
                         icon_url= target.avatar_url)
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        embed.add_field(name = 'Joined Discord', value = joinDiscDate,inline = True)
        embed.add_field(name = 'Joined Server', value = joinServDate,inline = True)
        
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name='usercount',
                       pass_context = True,
                       description = "Output amount of users.")
    async def usercount(self,ctx):
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
                       pass_context = True,
                       description = "Listen to the song of our people.")
    async def oceanman(self, ctx):
        await ctx.send(f"{ctx.author.mention} BIG POG! \nhttps://www.youtube.com/watch?v=6E5m_XtCX3c")

    @commands.command(name = 'say',
                      pass_context = True,
                      description = "Have the bot say something.",
                      aliases=["announce"])
    async def say(self,ctx,*,msg):
        await ctx.message.delete()
        await ctx.send(msg)

def setup(client):
    print("Setting up General Cog...")
    client.add_cog(General(client))
