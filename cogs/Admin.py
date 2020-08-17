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

def setup(client):
    print("Setting up Admin Cog...")
    client.add_cog(Admin(client))
    