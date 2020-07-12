import discord
from discord.ext import commands

class Admin(commands.Cog):
    """Admin use commands."""
    def __init__(self,client):
        self.client = client
    
def setup(client):
    print("Setting up Admin Cog...")
    client.add_cog(Admin(client))
    