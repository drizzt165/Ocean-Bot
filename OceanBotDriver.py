import os

import disnake as discord
from disnake.ext import commands

# Load .env files
from dotenv import load_dotenv
load_dotenv()

class Client(commands.Bot):
    def __init__(self, command_prefix, help_command, intents):
        super().__init__(command_prefix, help_command, intents=intents)

    def load_cogs(self, client):
        for cog in [file.split('.')[0] for file in os.listdir("cogs") if file.endswith('.py')]:
            try:
                if cog != "__init__":
                    client.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(e)

    async def on_ready(self):
        print("Loading cogs...")
        self.load_cogs(self)
        await client.change_presence(status=discord.Status.online,
                                     activity=discord.Activity(type=discord.ActivityType.watching, name=f"for /help"))
        print("Bot is ready!")

    async def on_message(self, msg):
        # always have this in on_message or commands won't work
        await self.process_commands(msg)


if __name__ == "__main__":
    intents = discord.Intents.all()
    client = Client(command_prefix=None,
                    help_command=None,
                    intents=intents)
    client.run(os.getenv('TOKEN'))
