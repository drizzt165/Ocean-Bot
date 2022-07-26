import disnake as discord
from disnake.ext import commands

class Admin(commands.Cog):
    """Commands only available to admin users."""
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.red()
    
def setup(client):
    print("Setting up Admin Cog...")
    client.add_cog(Admin(client))
    