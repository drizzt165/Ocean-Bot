import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.red()
    
def setup(client):
    print("Setting up Admin Cog...")
    client.add_cog(Admin(client))
    