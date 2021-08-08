import asyncio
import discord
from discord.embeds import Embed
from discord.ext import commands
import random
from discord.utils import get
import os
import wonderwords
import datetime
import re

def text(description,format,usage):
    return f"**Description** : \n{description}\n\n**Format** : \n{format}\n\n**Usage** : \n```{usage}```"

class Basic(commands.Cog):
    """Basic Free verse command for all users"""
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors

    async def add(self,id,amount = 2000):
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE userid = $1",id)
        await self.bot.pg_con.execute("UPDATE users SET credits = $1 WHERE userid = $2",user[1]+amount,id)

    async def get(self,id):
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE userid = $1",id)
        return user[1]

    async def check(self,id):
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE userid = $1",id)
        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (userid, credits,bg) VALUES ($1,$2,$3)",id,2000,['default'])


    @commands.command()
    async def ping(self, ctx):
        """Check the bot latency"""
        embed = discord.Embed(description = f"<a:tick:819047828013056001> **|** Pong! I have a bot ping of: **{round(self.bot.latency * 1000)}ms**", color = random.choice(self.colors))
        embed.set_footer(text = "It's your turn now!")
        await ctx.send(embed = embed)


    @commands.command(aliases= ['th'])
    async def thank(self,ctx ,member: discord.Member,*,reason = "for your help"):
        """Thank a member with a reason for his/her help"""
        await self.check(ctx.author.id)
        await self.check(member.id)
        if await self.get(ctx.author.id)<200:
            em = discord.Embed(title = f"Not Sufficient Credits",description = f"{ctx.author.mention} doesn't have sufficient credits To Thank ",color = random.choice(self.colors))
            await ctx.send(embed = em,delete_after = 7)
            return
        em = discord.Embed(title = f"Congrataltions {member.name} :partying_face: ",description=f":tada: You have been Thanked by {ctx.author.name} {reason}  :tada:\n200 credits are Thanked to {member.mention} by {ctx.author.mention}",color = random.choice(self.colors) )
        await self.add(ctx.author.id,-200)
        await self.add(member.id,200)
        await ctx.send(embed=em)


    @commands.command()
    async def typerace(self, ctx):
        """Who's the fastest typer here? Check your WPM (words per minute)"""
        emojified = ''

        sentence = wonderwords.RandomSentence().sentence().replace(".","")
        length = len(sentence.split())
        formatted = re.sub(r'[^A-Za-z ]+', "", sentence).lower()
        
        for i in formatted:
            if i == ' ':
                emojified += '   '
            else:
                emojified += ':regional_indicator_{}: '.format(i)
        sent = await ctx.send(f"{emojified}.")

        def check(msg):
            return msg.content.lower() == sentence.lower()
        try:
            s = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed = discord.Embed(description = "No one answered Correct in time.", color = discord.Colour.red()))
        else:
            
            time =  str(datetime.datetime.utcnow() - sent.created_at)
            time_format = time[:-5][5:]
            if time_format[0] == '0':
                time_format = time_format[1:]
            
            embed = discord.Embed(description = f"{s.author.mention} Completed the typerace in **{time_format}** seconds.", color=random.choice(self.colors))
            time_in_mins = float(time_format)/60
            embed.add_field(name = "WPM (Words Per Minute) : ", value = int(length/time_in_mins))
            await ctx.send(embed = embed)
            
  
    @commands.command(aliases = ["suggestion"])
    async def suggest(self,ctx,*,suggestion):
        """Give a suggestion for the server"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await ctx.message.delete()
        id = await self.bot.pg_con.fetchrow("SELECT suggestionchannel FROM guild WHERE guildid = $1",ctx.guild.id)
        id = id[0]
        if id == None:
            await ctx.send(embed = discord.Embed(title = "Suggestion Channel Not Synced",description = f"You need to set the suggestion channel by sayin `{prefix}set_suggestion + #channel_name` to set the channel\nThen Type `{prefix}suggestion + suggestion` to send a suggestion into that specific channel ",color = 0x2F3136))
            return
        channel = self.bot.get_channel(id)
        em = discord.Embed(title = "Sugesstion : ",description = suggestion,timestamp = datetime.datetime.utcnow(),color = random.choice(self.colors))
        
        em.set_thumbnail(url = ctx.author.avatar_url)
        em.set_author(name = ctx.author.name)
        em.set_footer(text = f"Change the suggestion channel by {prefix}set_suggestion #channel_name and remove suggestion command by {prefix}remove_sug")
        message = await channel.send(embed = em)
        await message.add_reaction("✅")
        await message.add_reaction("❎")
        await ctx.send(f"Your Suggestion have been succesfully sent ! :)\nCheck <#{id}>",delete_after = 10)
        await asyncio.sleep(36000)
        agmessage = await channel.fetch_message(message.id)
        positive = await agmessage.reactions[0].users().flatten()
        positive.pop(positive.index(self.bot.user))
        negative = await agmessage.reactions[1].users().flatten()
        negative.pop(negative.index(self.bot.user))
        if len(positive)>len(negative):
            winner = "Proposition shall be followed"

        elif len(positive)<len(negative):
            winner = "Proposition shalln't be followed"

        else:
            winner = f"That was a Tie, Now all depends on {ctx.guild.owner.mention}"
        
        positive = "\n".join([str(i.mention) for i in positive]) 
        negative = "\n".join([str(i.mention) for i in negative]) 

        em2 = discord.Embed(title = "Poll Closed 🔒",color = 0x2F3136,timestamp = datetime.datetime.utcnow())
        em2.add_field(name = "Suggestion : ",value = suggestion,inline=False)
        em2.add_field(name = "People in Support : ",value=positive,inline=True)
        em2.add_field(name = "People in Opposition : ",value=negative,inline=True)
        em2.add_field(name = "Result",value=winner,inline=False)
        em2.set_footer(text=f"Remove suggestion command by {prefix}remove_sug")
        await channel.send(embed = em2)
        
    @commands.command(aliases = ['bug'])
    async def reportbug(self,ctx,*,bug):
        """Report a bug to the developer"""
        owner = get(self.bot.get_all_members(), id=779743087572025354)
        em = discord.Embed(title = "Bug Report",description = f"{bug}\nReported by {ctx.author.name} from {ctx.guild.name}",color = random.choice(self.colors))
        em.set_author(name = ctx.author.display_name , icon_url=ctx.author.avatar_url)
        try:
            await owner.send(embed = em)
            await ctx.send("Bug was Succesfully Recorded :slight_smile:  ",delete_after = 5)
        except Exception as e:

            await ctx.send(f"Message could not be sent , Try again later :( \n{e}",delete_after = 6)

    
def setup(bot):
    bot.add_cog(Basic(bot))
