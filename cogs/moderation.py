import discord
from discord.ext import commands
import random
import asyncio
from discord.utils import get

error = discord.Embed(title = "Invalid input or arguments !!\nType `.help` or `.more_help` for more info",color = discord.Colour.red()) 
        

class Moderation(commands.Cog):
    """For maintaining the decorum of the server"""
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors

    @commands.command(aliases= ['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member :discord.Member,*,reason = "No reason Provided"):
        """Ban a specific member"""
        em = discord.Embed(description = f"{member.mention} is Banned from {ctx.guild.name} by {ctx.author.mention} \n Reason : {reason}",color = discord.Colour.random() )
        em.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url =ctx.guild.icon_url)
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=em)
        except:
            await ctx.send(embed = discord.Embed(title= "Missing Permissions",description = f"Bot doesn't have the required Perms to Ban {member.name}",color = discord.Colour.red()))
        

    @commands.command(aliases= ['k'])
    @commands.has_permissions( kick_members=True)
    async def kick(self,ctx, member :discord.Member,*,reason = "No reason Provided"):
        """Kick a member"""
        em = discord.Embed(description = f"{member.mention} is Kicked from {ctx.guild.name} by {ctx.author.mention} \n Reason : {reason}",color = discord.Colour.random() )
        em.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        
        try:
            await member.send("https://discord.gg/UckPYtvqqc")
        except:
            pass
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=em)
        except:
            await ctx.send(embed = discord.Embed(title= "Missing Permissions",description = f"Bot doesn't have the required Perms to Ban {member.name}",color = discord.Colour.red()))
    @commands.command(aliases = ['ub'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unban(self,ctx, member):
        """Unban a member"""
        member_nam ,member_dis = member.split('#')
        em = discord.Embed(description = f"{member_nam} is Unbanned from {ctx.guild.name} by {ctx.author.name} ",color = discord.Colour.random() )
        em.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        banned = await ctx.guild.bans()
        member_nam ,member_dis = member.split('#')

        for banned_entry in banned:
            user = banned_entry.user

            if(user.name ,user.discriminator) == (member_nam,member_dis):
                await ctx.guild.unban(user)
                await ctx.send(embed = em)
                return

            await ctx.send(member + ' was not found',delete_after =4)
    @commands.command(aliases= ['m'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def mute(self,ctx,member:discord.Member,amount = 2):
        """Mute a member"""
        if ctx.author == member:
            await ctx.send("You can't mute yourself :lol:",delete_after=4)
            return
        if member == self.bot.user:
            await ctx.send("You can't make me mute myself :lol:",delete_after=4)
            return

        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        try:
            muted = get(ctx.guild.roles,name="Muted")
        except:
            await ctx.send(embed = discord.Embed(title = "No role Named Muted",description= f"Type `{prefix}mutedrole` or `{prefix}createmute` to create a muted Role \nThe bot will automatically Take it's messaging rights",color = random.choice(self.colors)))
            return
        if muted in member.roles:
            await ctx.send(f"{member.name} is already Muted !!")
        else:
            em2 = discord.Embed(title = "Member Muted !",description =f"{member.mention} is muted by {ctx.author.mention} for {amount} min(s)   ",color = discord.Colour.random())   
            em2.set_thumbnail(url=ctx.guild.icon_url) 
            em2.set_footer(icon_url= ctx.guild.icon_url, text= f"From {ctx.guild.id}")   
            em3 = discord.Embed(title = "Member Unmuted !",description =f"{member.mention} is Unmuted Now",color = discord.Colour.random())   
            em3.set_thumbnail(url=ctx.guild.icon_url) 
            em3.set_footer(icon_url= ctx.guild.icon_url, text= f"From {ctx.guild.id}")  
            try:
                amount = float(amount)*60

                await member.add_roles(muted)
                await ctx.send(embed=em2)
                try:
                    await member.send(embed = em2)
                except:
                    pass
                await asyncio.sleep(amount)
                await member.remove_roles(muted)
                await ctx.send(embed=em3)
            except:
                await ctx.send(embed=error)

    
    @commands.command(aliases= ['um'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unmute(self,ctx,member:discord.Member):
        """Unmute a member"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        try:
            muted = get(ctx.guild.roles,name="Muted")
        except:
            await ctx.send(embed = discord.Embed(title = "No role Named Muted",description= f"Type `{prefix}mutedrole` or `{prefix}createmute` to create a muted Role \nThe bot will automatically Take it's messaging rights",color = random.choice(self.colors)))
            return
        em3 = discord.Embed(title = "Member Unmuted !",description =f"{member.mention} is Unmuted Now",color = discord.Colour.random())   
        em3.set_thumbnail(url=ctx.guild.icon_url) 
        em3.set_footer(icon_url= ctx.guild.icon_url, text= f"From {ctx.guild.name}")  
        if muted in member.roles:
            await member.remove_roles(muted)
            await ctx.send(embed=em3)

        else:
            await ctx.send("Member is already Unmuted !!",delete_after=4)
    
    @commands.command(aliases= ['c'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def clear(self,ctx,amount):
        """Clear chats"""
        try:
            amount = int(amount)
            if amount>5000:
                return await ctx.send("Cannot delete messages more than 5000",delete_after=10)
    
            if amount < 1:
                return await ctx.send('Amount should be at least 1!!')
            if amount > 100:
                
                await ctx.message.reply(f"Are you sure wanna delete {amount} messages? (y/n)")
                try:
                    msg = await self.bot.wait_for('message',timeout = 10.0,check =lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    return await ctx.send("Recieved no answer, Aborting.....",delete_after=20)
                else:
                    if msg.content.lower()=="y":
                        await ctx.channel.purge(limit = amount+3)
                    return
            else:
                return await ctx.channel.purge(limit = amount+1)
        except:
            return await ctx.send(embed = error)



def setup(bot):
    bot.add_cog(Moderation(bot))
