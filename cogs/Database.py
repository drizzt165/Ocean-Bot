import dotenv
import discord
from datetime import datetime
from discord.ext import commands

class Database(commands.Cog):
    """Commands to interact with the SQL database."""
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.blue()

    @commands.command(name = 'test',
                      pass_context = True)
    async def test(self,ctx):
        pass

def setup(client):
    print("Setting up Database Cog...")
    client.add_cog(Database(client))