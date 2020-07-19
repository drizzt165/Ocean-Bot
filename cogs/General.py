import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.EmbedColour = discord.Colour.orange()
        
    @commands.command(name = 'help',
                      pass_context = True,
                      description = "Print list of commands.")
    async def help(self,ctx,msg = None):
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        commands = [command for command in self.client.commands 
                    if command.name != 'help' and
                    command.description and
                    command.name]
        commandNames = [command.name for command in commands]
            
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        if not msg:
            embed.set_author(name = 'Ocean-Bot Commands')
            for command in commands:
                embed.add_field(name = f"!{command.name}",
                                value = command.description,
                                inline = False)                   
        elif msg in commandNames:
            commandIndx = commandNames.index(msg)
            curCommand = commands[commandIndx]
            
            embed.add_field(name = f"!{msg}",
                            value = curCommand.description,
                            inline = False)
            if curCommand.brief:
                embed.add_field(name = "Example:", value = curCommand.brief)
            if curCommand.aliases:
                embed.add_field(name = "Aliases", value = ','.join([al for al in curCommand.aliases]))
        else:
            embed.set_author(name = f"Command !{msg} does not exist.")
        
        await ctx.message.delete()
        await ctx.send(embed=embed) 
    
    @commands.command(name = 'user',
                      pass_context = True,
                      description = "Output stats of mentioned member.",
                      brief = "!user @<member>")
    async def user(self,ctx,msg=None):
        if msg:
            target = ctx.message.mentions[0]
        else:
            target = ctx.author
        joinDiscDate = str(target.created_at).split(' ')[0]
        joinServDate = str(target.joined_at).split(' ')[0]
        
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        userIcon = discord.File("Images/User.png",filename = "User.png")
        
        embed.set_author(name=f"{target}", 
                         icon_url = "attachment://User.png")
        embed.set_thumbnail(url = target.avatar_url)
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        embed.add_field(name = 'Joined Discord', value = joinDiscDate,inline = True)
        embed.add_field(name = 'Joined Server', value = joinServDate,inline = True)
        
        await ctx.message.delete()
        await ctx.send(file = userIcon, embed=embed)

    @commands.command(name='userstatus',
                       pass_context = True,
                       description = "Output amount of users.")
    async def userstatus(self,ctx):
        guild = ctx.author.guild
        totalMembers = guild.member_count
        onlineMembers = offlineMembers = idleMembers = dndMembers=0

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
        
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        titleIcon = discord.File("Images/Community.png",filename = 'Community.png')
        
        embed.set_author(name = f"Current member status ({totalMembers})",
                          icon_url = "attachment://Community.png")
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        embed.add_field(name = 'Online:', value = onlineMembers,inline= True)
        embed.set_image(url="attachment://OnlineIcon.png")
        embed.add_field(name = 'Offline:', value = offlineMembers,inline = True)
        embed.add_field(name = 'Idle/DND:', value = idleMembers+dndMembers,inline = True)
        
        await ctx.message.delete()
        await ctx.send(file = titleIcon, embed = embed)

    @commands.command(name='oceanman',
                       pass_context = True,
                       description = "Listen to the song of our people.")
    async def oceanman(self, ctx):
        await ctx.send(f"{ctx.author.mention} BIG POG! \nhttps://www.youtube.com/watch?v=6E5m_XtCX3c")

    @commands.command(name = 'say',
                      pass_context = True,
                      description = "Have the bot say something.",
                      aliases=["announce"],
                      brief = "!say <content to echo>")
    async def say(self,ctx,*,msg):
        await ctx.message.delete()
        await ctx.send(msg)

def setup(client):
    print("Setting up General Cog...")
    client.add_cog(General(client))
