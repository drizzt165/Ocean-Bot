import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, Cog
import datetime


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
    