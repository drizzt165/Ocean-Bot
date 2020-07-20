import sys
import os
import discord
from discord.ext import commands
from PyDictionary import PyDictionary
import configparser
from customPackages.urbandict import UrbanDic

class Dictionary(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.initConsts()
        self.EmbedColour = discord.Colour.green()
        self.dic = PyDictionary()
        self.udic = UrbanDic()
        
    def initConsts(self):
        config = configparser.ConfigParser()
        config.read('settings.cfg')
        self.AntonymSynonymCount = int(config['DICTIONARY']['AntonymSynonymCount'])
        self.DictionaryMeaningLimit = int(config['DICTIONARY']['DictionaryMeaningLimit'])
        
    @commands.command(name = 'udefine',
                      description = "Urban Dictionary of a given word.",
                      pass_context = True,
                      brief = "!def <word>",
                      aliases = ['udef'])
    async def udefine(self,ctx,msg=None):
        cmd = ctx.message.content.split()[0]
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        if msg:
            wordData = self.udic.define(msg) #Only save top result
            if wordData:
                wordData = wordData[0]
                embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
                embed.set_author(name = 'Urban Dictionary:')
                embed.add_field(name = wordData.word,
                                value = wordData.meaning,
                                inline = False)
                embed.add_field(name = 'Example:',
                                    value = wordData.example,
                                    inline = False)
            else:
                embed.set_author(name = f'No definition found for \"{msg}\"')      
        else:
            embed.add_field(name = 'Command misuse', 
                            value = f'Please add a word after \"{cmd}\"')
        
        await ctx.message.delete()
        await ctx.send(embed = embed)
    
    @commands.command(name = 'define',
                      description = "Define a given word.",
                      pass_context = True,
                      brief = "!def <word>",
                      aliases = ['def'])
    async def define(self,ctx,msg = None):
        cmd = ctx.message.content.split()[0]
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        if msg:
            meaning = self.dic.meaning(term = msg, disable_errors=True)
            if meaning:
                embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
                embed.set_author(name = f"Definition for \"{msg}\":")         
                for k in meaning.keys():
                    for x,m in enumerate(meaning[k]):
                        if x < self.DictionaryMeaningLimit:
                            embed.add_field(name = k,value = m)
            else:
                embed.set_author(name = f"No definition found for \"{msg}\"")
        else:
            embed.add_field(name = 'Command Misuse:', value = f"Please add a word to define after {cmd}.")

        await ctx.message.delete()
        await ctx.send(embed = embed)
    
    @commands.command(name = 'synonym',
                      pass_context = True,
                      description = "Print synonyms of a given word.",
                      brief = "!synonym <word>",
                      aliases = ['syn'])
    async def synonym(self,ctx,msg=None):
        cmd = ctx.message.content.split()[0]
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        if msg:
            synonyms = self.dic.synonym(term = msg)
            if synonyms:
                result = 'Blank'
                if len(synonyms) < self.AntonymSynonymCount:
                    result = ', '.join(synonyms)
                else:
                    result = ', '.join(synonyms[0:self.AntonymSynonymCount])
                embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
                embed.add_field(name = f'Synonyms for "{msg}"',
                                value = result,
                                inline=True)
            else:
                embed.set_author(name = f'No synonyms for "{msg}"')
        else:
            embed.add_field(name = 'Command Misuse:',
                            value = f"Please add a word to define after {cmd}.",
                            inline=True)
        
        await ctx.message.delete()
        await ctx.send(embed = embed)
    
    @commands.command(name = 'antonym',
                      pass_context = True,
                      description = "Print antonyms of a given word.",
                      brief = "!antonym <word>",
                      aliases = ['ant'])
    async def antonym(self,ctx,msg=None):
        cmd = ctx.message.content.split()[0]
        embed = discord.Embed(
            colour = self.EmbedColour
        )
        if msg:
            antonyms = self.dic.antonym(term = msg)
            if antonyms:
                result = 'Blank'
                if len(antonyms) < self.AntonymSynonymCount:
                    result = ', '.join(antonyms)
                else:
                    result = ', '.join(antonyms[0:self.AntonymSynonymCount])
                embed.set_footer(text= f"Requested by {ctx.author}",icon_url= ctx.author.avatar_url)
                embed.add_field(name = f'Antonyms for "{msg}"',
                            value = result,
                            inline=True)
            else:
                embed.set_author(name = f'No antonyms for "{msg}"')
        else:
            embed.add_field(name = 'Command Misuse:',
                            value = f"Please add a word to define after {cmd}.",
                            inline=True)
        
        await ctx.message.delete()
        await ctx.send(embed = embed)
    
def setup(client):
    print("Setting up Dictionary Cog...")
    client.add_cog(Dictionary(client))
    