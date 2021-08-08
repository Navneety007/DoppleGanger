import animec
import discord
import datetime
from discord.ext import commands
import random
from discord.ext.commands.core import command

class Anime(commands.Cog):
    """Anime commmands for weebs"""
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors

    @commands.command()
    async def anime(self,ctx,*,query):
        """Search any Anime for info regarding Rating, Episodes, Status etc."""
        try:
            anime = animec.Anime(query)
        except:
            await ctx.send(embed=  discord.Embed(description = "No corresponding Anime is found for the search query",color = discord.Color.red()))
            return
        embed = discord.Embed(title = anime.title_english,url = anime.url,description = f"{anime.description[:200]}...",color = random.choice(self.colors))
        embed.add_field(name = "Episodes",value = str(anime.episodes))
        embed.add_field(name = "Rating",value = str(anime.rating))
        embed.add_field(name = "Broadcast",value = str(anime.broadcast))
        embed.add_field(name = "Status",value = str(anime.status))
        embed.add_field(name = "Type",value = str(anime.type))
        embed.add_field(name = "NSFW status",value = str(anime.is_nsfw()))
        embed.set_thumbnail(url = anime.poster)
        await ctx.send(embed = embed)

    @commands.command(aliases = ["char","animecharacter"])
    async def image(self,ctx,*,query):
        """Search any anime Character"""
        try:
            char = animec.Charsearch(query)
        except:
            await ctx.send(embed=  discord.Embed(description = "No corresponding Anime Character is found for the search query",color = discord.Color.red()))
            return

        embed = discord.Embed(title = char.title,url = char.url,color = random.choice(self.colors))
        embed.set_image(url = char.image_url)
        embed.set_footer(text = ", ".join(list(char.references.keys())[:2]))
        await ctx.send(embed = embed)

    
    @commands.command(aliases = ['lyric'])
    async def lyrics(self,ctx,*,song):
        url = animec.sagasu._searchLyrics_(song)
        await ctx.send(url)

    @commands.command()
    async def aninews(self,ctx,amount:int=3):
        """Get updated with the latest news regarding Anime Industry"""
        if amount>9:
            return await ctx.send("Please keep the amount less than 9 at a time to avoid spamming")
        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        descriptions = news.description
        
        embed = discord.Embed(title = "Latest Anime News",color = random.choice(self.colors),timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url=news.images[0])

        for i in range(amount):
            embed.add_field(name = f"{i+1}) {titles[i]}", value = f"{descriptions[i][:200]}...\n[Read more]({links[i]})",inline=False)

        await ctx.send(embed = embed)

        

def setup(bot):
    bot.add_cog(Anime(bot))