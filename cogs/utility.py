import discord
from discord.ext import commands
import random
from discord.ext.commands.core import command
import datetime
from discord.utils import get


class Utility(commands.Cog):
    """Utility commands for setting up the environment"""
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors

    @commands.command()
    @commands.has_permissions(kick_user = True)
    async def setprefix(self, ctx,*,prefix='.'):
        """Set bot prefix"""
        await self.bot.pg_con.execute("UPDATE guild SET prefix = $1 WHERE guildid = $2",prefix,ctx.guild.id)
        await ctx.message.reply(f"PREFIX updated to `{prefix}`")

    @commands.command(aliases = ['mainchannel'])
    @commands.has_permissions(administrator=True) 
    async def setmain(self,ctx,channel:discord.TextChannel):
        """Set the main channel for welcomes, updates etc"""
        await self.bot.pg_con.execute("UPDATE guild SET mainchannel = $1 WHERE guildid = $2",channel.id,ctx.guild.id)
        embed = discord.Embed(title = "Main Channel Updated",description = f"Main channel has been set to {channel.mention}",color = random.choice(self.colors))
        await ctx.send(embed = embed)

    @commands.command(aliases = ['sugchannel'])
    @commands.has_permissions(administrator=True) 
    async def setsuggestion(self,ctx,channel:discord.TextChannel):
        """Set a channel for sending suggestions (in order to use the `suggest` command)"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await self.bot.pg_con.execute("UPDATE guild SET suggestionchannel = $1 WHERE guildid = $2",channel.id,ctx.guild.id)
        embed = discord.Embed(title = "Suggestion Channel Updated",description = f"Suggestion channel has been set to {channel.mention}\nNow Type `{prefix}suggest + [suggestion]` without these '[',']' to Send a suggestion into the channel and start a Poll",color = random.choice(self.colors))
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['aichannel'])
    @commands.has_permissions(administrator=True) 
    async def setaichatbot(self,ctx,channel:discord.TextChannel):
        """Set AI-chatbot channel to chat with AI"""
        await self.bot.pg_con.execute("UPDATE guild SET aichannel = $1 WHERE guildid = $2",channel.id,ctx.guild.id)
        embed = discord.Embed(title = "AI-chatbot Channel Updated",description = f"Now Enjoy talking with AI chabot in {channel.mention}\nYou can start talking to the Chatbot now. Why not start with sayin 'HI' or something :)",color = random.choice(self.colors))
        await ctx.send(embed = embed)

    @commands.command(aliases = ['logchannel'])
    @commands.has_permissions(administrator=True) 
    async def setlogs(self,ctx,channel:discord.TextChannel):
        """Set logs channel to get update with logs"""
        await self.bot.pg_con.execute("UPDATE guild SET logchannel = $1 WHERE guildid = $2",channel.id,ctx.guild.id)
        embed = discord.Embed(title = "Log Channel Updated",description = f"Log channel has been set to {channel.mention}\nNow get the Information regarding the status, activity, Nickname, Roles, Pending of every person in the server",color = random.choice(self.colors))
        await ctx.send(embed = embed)

    
    @commands.command(aliases = ['remove_logs'])
    @commands.has_permissions(administrator=True) 
    async def remove_log(self,ctx):
        """Remove the logs channel"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await self.bot.pg_con.execute("UPDATE guild SET logchannel = $1 WHERE guildid = $2",None,ctx.guild.id)
        await ctx.send(embed = discord.Embed(title = "Logging Turned Off",description = f"Logging Has been Deactivated, This server won't be updated with the user's activity, status, roles, nickname anymore\nType `{prefix}set_logs #log_channel` to start enojoying the Features again ",color = random.choice(self.colors)))
    
    @commands.command(aliases = ['remove_suggestion'])
    @commands.has_permissions(administrator=True) 
    async def remove_sug(self,ctx):
        """Remove the suggestion channel and the command"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await self.bot.pg_con.execute("UPDATE guild SET suggestionchannel = $1 WHERE guildid = $2",None,ctx.guild.id)
        await ctx.send(embed = discord.Embed(title = "Suggestion Command Turned Off",description = f"Suggestions Have been Deactivated, You won't be able to use Suggestion command in 'tis server now\nType `{prefix}set_suggestion #suggestion_channel` to start enojoying the Command again",color = random.choice(self.colors)))

    @commands.command(aliases = ['remove_aichatbot'])
    @commands.has_permissions(administrator=True) 
    async def remove_aibot(self,ctx):
        """Remove the AI-chatbot channel"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await self.bot.pg_con.execute("UPDATE guild SET aichannel = $1 WHERE guildid = $2",None,ctx.guild.id)
        await ctx.send(embed = discord.Embed(title = "AI-Chatbot Turned Off",description = f"AI-chabot features Have been Deactivated, You won't be able to enjoy Chatbot Features now\nType `{prefix}set_aichatbot #Aichatbot_channel` to start enojoying the features again",color = random.choice(self.colors)))

    @commands.command(aliases = ['remove_general'])
    @commands.has_permissions(administrator=True) 
    async def remove_main (self,ctx):
        """Remove the general/main channel"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await self.bot.pg_con.execute("UPDATE guild SET mainchannel = $1 WHERE guildid = $2",None,ctx.guild.id)
        await ctx.send(embed = discord.Embed(title = "Main-Channel features Turned Off",description = f"Now you won't be getting any welcome commands, leave-join events, drops etc\nType `{prefix}set_main #main_name` to enjoy these features again ",color = random.choice(self.colors)))

    @commands.command(aliases = ['invite'])
    async def join(self,ctx):
        """Join our main channel or invite this bot"""
        embed = discord.Embed(title = "Invite",timestamp = datetime.datetime.utcnow(),color = random.choice(self.colors))
        embed.add_field(name="Invite This Bot to your server",value="[Click Here to Invite](https://discord.com/api/oauth2/authorize?client_id=781737639321141268&permissions=4228906103&scope=bot)",inline=False)
        embed.add_field(name="Join our Main Server",value="[Click Here to join](https://discord.gg/cRGWDtu3W8)",inline=False)
        embed.set_image(url=self.bot.user.avatar_url)
        owner = get(self.bot.users , id = 779743087572025354)
        embed.set_thumbnail(url = owner.avatar_url)
        await ctx.send(embed = embed)
    

    @commands.command(aliases = ['createmute'])
    @commands.has_permissions(administrator=True) 
    async def mutedrole(self,ctx):
        """Create the muted role to use mute command"""
        try:
            muted = get(ctx.guild.roles,name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages = False) 
            await ctx.send("Muted Role Existed, Purged it's Perms to send Messages into any channel")
        except:   
            await ctx.guild.create_role(name = "Muted",colour = 0xFF0C00)
            muted = get(ctx.guild.roles, name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages = False) 
            await ctx.send("Muted Role Created! , Purged it's Perms as well to send Messages into any channel")


def setup(bot):
    bot.add_cog(Utility(bot))
