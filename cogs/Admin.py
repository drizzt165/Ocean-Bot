import dotenv
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, Cog

class Admin(commands.Cog):
    """Commands only available to admin users."""
    @has_permissions(administrator = True)
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.red()
        self.dbManager = self.client.dbManager

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

    @commands.command(name = 'test',
                      pass_context = True)
    async def test(self,ctx):
        tables = self.dbManager.get_tables()
        self.dbManager.init_table(ctx)
        self.dbManager.init_rows(ctx)

        print(tables)

    
def setup(client):
    print("Setting up Admin Cog...")
    client.add_cog(Admin(client))
    