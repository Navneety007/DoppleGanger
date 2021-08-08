import asyncio
import discord
from discord.ext import commands
import random
from discord.ext.commands.core import command
import praw
import wolframalpha
from youtubesearchpython import SearchVideos
from pytube import YouTube
from youtube_search import YoutubeSearch
import animec
import os


client1 = wolframalpha.Client("LH6XXP-3U64EU2EHX") 
reddit = praw.Reddit(client_id = "laqA2QEwsdXP9A",
                    client_secret = "z6NHXe06ch_h8Iyn2mtbn1FkIJ4pfg",
                    username  = "DopplegangerCode ",
                    password = "elpsycongree",
                    user_agent = "pythonpraw", check_for_async=False)

memes = ['programminghumor','animememes','weebmemes','goodanimemes','danidev','funnymeme','sarcasticmemes','lolmemes','codinghumor']


class Search(commands.Cog):
    """Search several stuff"""
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors


    @commands.command(aliases = ['me'])
    async def meme(self,ctx):
        """Search a meme"""
        try:
            subreddit = reddit.subreddit(random.choice(memes)) 
            all_subs = []
            top = subreddit.top(limit = 100)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            embed = discord.Embed(title = random_sub.title, color = random.choice(self.colors))
            embed.set_image(url = random_sub.url)
            embed.set_footer(text = f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
            
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(e)
            em = discord.Embed(title = "No Meme Found :sob:",color = random.choice(self.colors))
            await ctx.send(embed = em)

    
    @commands.command()
    async def song(self,ctx, *, songname):
        """Search and download a song"""
        result = YoutubeSearch(songname, max_results=1).to_dict()
        name = result[0]["title"]
        url = "http://www.youtube.com"+result[0]["url_suffix"]
        try:
            
            yt = YouTube(url)
            print("trying")
            ys = yt.streams.filter(only_audio=True).first().download()
            print("Downloading")
            audio = name + ".mp3"
            os.rename(name+".mp4", audio)
            await ctx.send(file = discord.File(audio))
            os.remove(audio)
        
        except Exception as e:
            await ctx.send(e)
            await ctx.send(embed  =discord.Embed(description = "Song Couldn't be Found :(",color = discord.Colour.red()))
              
              
    @commands.command(aliases = ['question'])
    async def ques(self,ctx,*,ques):
        """Ask/search for a question"""
        emerror = discord.Embed(title ="No result found !! :sob:",color = discord.Color.red())
        ques = ques.lower()
        if "who made you" in ques or "who created you" in ques or "who is your creator"in ques :
            em = discord.Embed(title = f"Question : "+ ques +":question:",
                        description = f"answer : "+ "I was made by Code Stacks the great right in his PC!!"+ ":exclamation:",color = random.choice(self.colors))
            await ctx.send(embed = em) 
        else: 
            try:
                res = client1.query(ques)
                answer = next(res.results).text
            
                em = discord.Embed(title = f"Question : "+ ques +":question:",
                            description = f"answer : "+ str(answer)+ ":exclamation:",color = random.choice(self.colors))
                await ctx.send(embed = em)  
            except:
                await ctx.send(embed = emerror)
    

    @commands.command(aliases =['yo'])
    async def youtube(self,ctx,*,search_query):
        """Search youtube"""
        try:
            results = SearchVideos(search_query,mode="dict",max_results =1).result()
            title = results['search_result'][0]['title']
            channel = results['search_result'][0]['channel']
            duration = results['search_result'][0]['duration']
            views = results['search_result'][0]['views']
            time = results['search_result'][0]['publishTime']

            embed = discord.Embed(
                title ="Top Results for your search :",
                description = f"{title}\nChannel : {channel}\nTitle : {title}\nDuration : {duration}\nViews : {views}\nPublish Time : {time} " ,
                color = random.choice(self.colors)
                )
            await ctx.send(embed = embed)
            await ctx.send('Link : '+results['search_result'][0]['link']) 
        except Exception as e:
            await ctx.send(e)
            c = discord.Embed(title ="No results found :sob:",color = discord.Color.red()    )
            await ctx.send(embed = c)
    





def setup(bot):
    bot.add_cog(Search(bot))



