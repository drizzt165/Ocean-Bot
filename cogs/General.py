import discord
from discord.ext import commands
from datetime import datetime
import customPackages.utilityFunctions as util
import math


class General(commands.Cog):
    """General use commands for available to all users."""
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
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        
        
        cogDict = {}
        #ensure that all cog keys are capitalized
        for key,val in self.client.cogs.items():
            cogDict[key.capitalize()] = val
        
        commands = [c for c in self.client.commands if c.name != 'help']
        commandNames = [c.name for c in commands]

        if not msg: #print default help window
            embed.add_field(name = 'Ocean-Bot Commands',
                            value = f'{self.client.command_prefix}help <command> to get additional information for specific command.')
            for key,cog in cogDict.items():
                cogCmds = cog.get_commands()
                if cogCmds:
                    cmdNames = ', '.join([c.name for c in cogCmds if c.name != 'help'])
                    embed.add_field(name = key, value = cmdNames,inline = False)
        elif msg.capitalize() in cogDict.keys(): #Print cog data
            msgCog = msg.capitalize()
            embed.set_author(name = f'{msgCog} Commands')
            embed.add_field(name = 'Description: ', value = cogDict[msgCog].description,inline = False)
            
            cogCmds = cogDict[msgCog].get_commands()
            if cogCmds:
                embed.add_field(name = 'Commands: ', 
                                value = ', '.join([c.name for c in cogCmds if c.name != 'help']), 
                                inline = False)
            
        elif msg.lower() in commandNames: #print specific command data
            msgCmd = commands[commandNames.index(msg.lower())]
            embed.set_author(name = f'{self.client.command_prefix}{msgCmd} command')
            if msgCmd.description:
                embed.add_field(name = 'Description: ', value = msgCmd.description, inline = False)
            if msgCmd.brief:
                embed.add_field(name = 'Example: ', value = msgCmd.brief,inline = False)
        else:
            embed.set_author(name = f'No command or category named "{msg}"')
        
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
            
        todayDate = datetime.now().date()
        joinDiscDate = target.created_at.date()
        joinDiscDiff = util.format_YY_MM_DD((todayDate-joinDiscDate).days)
        
        joinServDate = target.joined_at.date()
        joinServDiff = util.format_YY_MM_DD((todayDate-joinServDate).days)
        
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        userIcon = discord.File("Images/User.png",filename = "User.png")
        
        embed.set_author(name=f"{target}", 
                         icon_url = "attachment://User.png")
        embed.set_thumbnail(url = target.avatar_url)
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        embed.add_field(name = 'Joined Discord', value = f"{joinDiscDate}\n{joinDiscDiff}",inline = True)
        embed.add_field(name = 'Joined Server', value = f"{joinServDate}\n{joinServDiff}",inline = True)
        embed.add_field(name = 'Mention ID: ', value = target.id,inline = False)
        
        await ctx.message.delete()
        await ctx.send(file = userIcon, embed=embed)

    @commands.command(name = 'server',
                       description = 'Print server info',
                       pass_context = True)
    async def server(self,ctx):
        embed = discord.Embed(colour = self.EmbedColour)
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        guild = ctx.message.guild
        
        embed.set_author(name = guild.name)
        embed.set_thumbnail(url = guild.icon_url)
        embed.add_field(name = ':id: Server ID: ', value = guild.id,inline = True)
        
        creationDate = guild.created_at.date()
        creationTime = guild.created_at.time().strftime("%I:%M %p")
        days = (datetime.now()-guild.created_at).days

        dateString = f"{creationDate} {creationTime}\n"
        dateString+=util.format_YY_MM_DD(days)
        
        embed.add_field(name = ':calendar: Created on: ', value = dateString)
        embed.add_field(name = ':crown: Owned by: ', value = guild.owner,inline = True)
        
        voiceChanCnt = len(guild.voice_channels)
        txtChanCnt = len(guild.text_channels)
        totalMembers = onlineMembers = 0
        for m in guild.members:
            if not m.bot:
                totalMembers+=1
                if m.status == discord.Status.online:
                    onlineMembers += 1
                
        embed.add_field(name = f":speech_balloon: Channels: {voiceChanCnt+txtChanCnt}", value = f"{voiceChanCnt} Voice | {txtChanCnt} Text", inline = True)
        embed.add_field(name = f":busts_in_silhouette: Members ({totalMembers}): ", value = f"{onlineMembers} Online",inline = True)
        embed.add_field(name = f':earth_africa: Region: ', value = guild.region)
        
        await ctx.message.delete()
        await ctx.send(embed = embed)

    @commands.command(name='userstatus',
                       pass_context = True,
                       description = "Output amount of users.")
    async def userstatus(self,ctx):
        guild = ctx.author.guild
        totalMembers = onlineMembers = offlineMembers = idleMembers = dndMembers=0

        for mem in guild.members:
            memStatus = mem.status
            if not mem.bot:
                totalMembers+=1
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

    @commands.command(name = 'inviteLink',
                      pass_context = True,
                      description = "DM invite bot link.")
    async def inviteLink(self,ctx):
        inviteURL = 'https://discord.com/api/oauth2/authorize?client_id=731385353021292564&permissions=8&scope=bot'
        inviteMsg = f"Join the Ocean-Bot family here:\n{inviteURL}"
        await ctx.message.delete()
        await ctx.author.send(inviteMsg)

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
