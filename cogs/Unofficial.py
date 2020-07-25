import discord
from discord.ext import commands

class Unofficial(commands.Cog):
    """Commands used for purposes relating directly to the Ocean Peoples Guild"""
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.dark_gold()
        
    @commands.command(name = 'albiononline',
                  pass_context = True,
                  description = 'Albion online copy-pasta.',
                  brief = '!albiononline simply outputs a copy pasta curated by Torpaydo')
    async def albiononline(self,ctx):
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        copyPasta = "Basically it is a classless mmo where your"\
                "weapon determines your main 3 damage/healing spells, "\
                "then you have helm/chest/feet that determine 3 of "\
                "your utility abilities. It has grindy things like "\
                "mining, woodcutting, and herbalism. But that is "\
                "all optional. A big appeal is there are 4 types "\
                "of zones. Green, yellow, red, and black. You are "\
                "safe in green zones. In yellow zones you can get "\
                "ganked, but if you do you just lose some cash. "\
                "In red and black zones if you get ganked you "\
                "lose everything you have on you \nAnd the "\
                "appeal to going into the higher risk zones is "\
                "that you get more experience and loot"
        steamURL = "https://store.steampowered.com/app/761890/Albion_Online/"
        albIcon = discord.File("Images/Albion.png",filename = "Albion.png")
        
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        embed.set_thumbnail(url = 'attachment://Albion.png')
        embed.add_field(name = 'Albion Online: ', 
                        value = copyPasta, 
                        inline = False)
        embed.add_field(name = 'Start your adventure TODAY!', 
                        value = steamURL, 
                        inline = False)
        
        await ctx.message.delete()
        await ctx.send(embed = embed, file = albIcon)
    
def setup(client):
    print("Setting up Unofficial Cog...")
    client.add_cog(Unofficial(client))
    