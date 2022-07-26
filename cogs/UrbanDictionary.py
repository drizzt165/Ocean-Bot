import sys
import os
import discord
from discord.ext import commands
from customPackages.urbandict import UrbanDic
from customPackages import utilityFunctions as util

class UrbanDictionary(commands.Cog):
    """Dictionary commands to expand your knowledge on slang and language in general."""
    def __init__(self,client):
        self.client = client
        self.EmbedColour = discord.Colour.green()
        self.udic = UrbanDic()
    
    @commands.command(name = 'ud_wotd',
                      description = 'Print the word of the day for Urban Dictionary!',
                      pass_context = True,
                      brief = "!ud_wotd <noArgs>")
    async def ud_wotd(self,ctx):
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        
        wotd = self.udic.WOTD()
        embed.set_author(name = f'Urban Dictionary: Word of the Day')
        embed.add_field(name = wotd.word,
                        value = util.truncateEmbedValue(wotd.meaning), 
                        inline = False)
        embed.add_field(name = "Example:",
                        value = util.truncateEmbedValue(wotd.example), 
                        inline = False)        
        
        await ctx.message.delete()
        await ctx.send(embed = embed)
    
    @commands.command(name = 'udefine',
                      description = "Urban Dictionary of a given word.",
                      pass_context = True,
                      brief = "!def <word>",
                      aliases = ['udef'])
    async def udefine(self,ctx,*,msg=None):
        cmd = ctx.message.content.split()[0]
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
        if msg:
            wordData = self.udic.define(msg) #Only save top result
            if wordData:
                wordData = wordData[0]
                embed.set_author(name = 'Urban Dictionary:')
                embed.add_field(name = wordData.word,
                                value = util.truncateEmbedValue(wordData.meaning),
                                inline = False)
                embed.add_field(name = 'Example:',
                                    value = util.truncateEmbedValue(wordData.example),
                                    inline = False)
            else:
                embed.set_author(name = f'No definition found for \"{self.udic.word}\"')      
        else:
            embed.add_field(name = 'Command misuse', 
                            value = f'Please add a word after \"{cmd}\"')
        
        await ctx.message.delete()
        await ctx.send(embed = embed)

def setup(client):
    print("Setting up Dictionary Cog...")
    client.add_cog(UrbanDictionary(client))
    