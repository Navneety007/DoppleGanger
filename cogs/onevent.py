import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw,ImageFont,ImageChops
from io import BytesIO
import random
from discord.utils import get
from chatterbot.trainers import ChatterBotCorpusTrainer,ListTrainer
from chatterbot import ChatBot
import traceback
from afks import afks

chatbot = ChatBot("DoppleGanger")
listtrainer = ListTrainer(chatbot)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english.greetings", 
              "chatterbot.corpus.english.conversations" )

def remove(afk):
    if "(AFK)" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

with open("./Assets/text/train.txt",'r',encoding="utf-8") as train:
    training = train.read().splitlines()

def circle(pfp,size = (220,220)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


invite = ["discord.gg","discord.com/invite"]
trainid = 21345654324
randomitem = [':soccer:',':boomerang:',':yo_yo:',':badminton:',':lacrosse:',':roller_skate:',':musical_keyboard:',':video_game:',':dart:',':jigsaw:',':violin:',':microphone:',':trophy:',':video_camera:',':film_frames:',':fire_extinguisher:',':syringe:',':magic_wand:',':pill:',':sewing_needle:']
roles = {"Commoners":400,"Gamer":400,"Anime Weeb":400,"Superior Coder":600,"Mods":400,"Partners":200,"Owner":1000}
toxic = ['nigga', 'retard', 'whore', 'faggot', 'nigger', 'nibba', 'dick', 'porn', 'squirt', 'hentai', 'penis', 'vagina', 'masturbate', 'boner' , 'bonner', 'pussy']

def revert(time):
    if time <= 86000 and time >3600:
        hrs = time//3600
        mins = (time%3600)/60
        return f"{int(hrs)} hr(s) {int(mins)} min(s)"
    elif time <= 3600 and time >60:
        times = time//60
        secs = (time%60)
        secs = str(secs)[:2]
        times = f"{int(times)} min(s) {secs} sec(s)"
        return times
    elif time<=60:
        return f"Only {int(time)} sec(s) Left !"


class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors

    async def train_data(self):
        data = await self.bot.pg_con.fetchrow("SELECT train FROM users WHERE userid = $1",trainid)
        if data[0] is None:
            return training
        return data[0]

   

    async def append(self,string):
        data = await self.bot.pg_con.fetchrow("SELECT train FROM users WHERE userid = $1",trainid)
        data = data[0]
        if data is None:
            data = []
        data.append(string)
        await self.bot.pg_con.execute("UPDATE users SET train = $1 WHERE userid = $2",set(data),trainid)
        
    async def check_guilds(self):
        columns = await self.bot.pg_con.fetch("SELECT guildid FROM guild")
        guilds = []
        if columns is None:
            pass
        else:
            for i in columns:
                guilds.append(i[0]) 


        for i in self.bot.guilds:
            if i.id not in guilds:
                await self.bot.pg_con.execute("INSERT INTO guild (guildid,prefix) VALUES ($1,$2)", i.id,".")


    async def starting(self):
        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS users (userid BIGINT NOT NULL, credits BIGINT , train TEXT[],inventory TEXT[],bg TEXT[])")
        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS guild (guildid BIGINT NOT NULL, prefix TEXT , mainchannel BIGINT,suggestionchannel BIGINT,aichannel BIGINT,logchannel BIGINT)")
        

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

    
    async def plus(self,id,name):
        data = await self.bot.pg_con.fetchrow("SELECT inventory FROM users WHERE userid = $1",id)
        data = list(data[0])
        data.insert(0,name)
        await self.bot.pg_con.execute("UPDATE users SET inventory = $1 WHERE userid = $2 ",data,id)
    
    @tasks.loop(seconds=3600*10)   
    async def interest(self):
        users = await self.bot.pg_con.fetch("SELECT * FROM users")
        for i in users:
            id = i[0]
            try:
                total =100
                await self.add(id,total)
                bgs = await self.available(id)
                if len(bgs)==0:
                    bgs = ['default']
                await self.update(id,bgs)
            except:
                continue   

    
    async def available(self,id):
        urls = await self.bot.pg_con.fetchrow("SELECT bg FROM users WHERE userid = $1",id)
        return urls[0]

    
    async def update(self,id,List):
        await self.bot.pg_con.execute("UPDATE users SET bg = $1 WHERE userid = $2",List,id)

    
    async def createlist (self):
        data = await self.bot.pg_con.fetch("SELECT train FROM users WHERE userid = $1",trainid)
        if not data:
            await self.bot.pg_con.execute("INSERT INTO users (userid, train) VALUES ($1,$2)",trainid,training)

    @commands.Cog.listener()
    async def on_ready(self):  
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Over {len([i for i in self.bot.get_all_members()])} members with shrewd powers"))   
        print("Here bot Comes :)")
        await self.starting()
        await self.createlist()
        await self.check_guilds()
        listtrainer.train(await self.train_data())
        await self.interest.start()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        columns = await self.bot.pg_con.fetch("SELECT guildid FROM guild")
        guilds=[]
        if columns==None:
            pass
        else:
            for i in columns:
                guilds.append(i)
        if guild.id not in guilds:
            await self.bot.pg_con.execute("INSERT INTO guild (guildid,prefix) VALUES ($1,$2)", guild.id,".")

        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",guild.id)
        prefix = prefix[0]
        for channel in guild.channels:
            if str(channel.type) == "text":
                if "general" in channel.name or "main" in channel.name:
                    await channel.send(f"Hi I am DoppleGanger :wave:\nThanks for Adding me Into {guild.name}. My Bot Prefix is `{prefix}` (Change it anytime By `{prefix}setprefix`) :partying_face: \nEnjoy Economy, Moderation, Welcome, Logs and many other such Commands :star_struck:\nType `{prefix}help` For more info\n\n-Code Stacks")
                    await self.bot.pg_con.execute("UPDATE guild SET mainchannel = $1 WHERE guildid = $2",channel.id,guild.id)
                    break
        await guild.create_role(name = "Muted",colour = 0xFF0C00)
        muted = get(guild.roles, name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(muted, send_messages = False) 


    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        guildid = member.guild.id
        if guildid==779743464774434857:
            commoner = get(member.guild.roles , id = 780294034098749470)
            await member.add_roles(commoner)
        channelid = await self.bot.pg_con.fetchrow("SELECT mainchannel FROM guild WHERE guildid = $1",guildid)
        if channelid[0] is None:
            return
        to = f"To {member.guild.name.title()}"
        if len(to)>19:
            to = f"{to[:19]}.."
        membername = member.name.title()
        if len(membername)>15:
            membername = f"{membername[:15]}.."
        asset = member.avatar_url_as(size = 256)
        asset2 = member.guild.icon_url_as(size = 256)
        data = BytesIO(await asset.read())
        data2 = BytesIO(await asset2.read())
        pfp = Image.open(data).convert("RGB")
        logo = Image.open(data2).convert("RGB")
        pfp.save("./Assets/images/profilereal.png")

        joined_at = "Joined at "+member.joined_at.strftime('%a, %#d %B %Y')
        logo = circle(logo,(200,200))
        pfp = circle(pfp,(296,296))
        welcome = Image.open('./Assets/images/welcome.png')
        welcome.paste(pfp,(898,216),pfp)
        welcome.paste(logo, (18, 18), logo)
        draw = ImageDraw.Draw(welcome)
        myFont = ImageFont.truetype('./Assets/fonts/Roboto-Regular.ttf', 110)
        myFont2 = ImageFont.truetype('./Assets/fonts/Roboto-Regular.ttf', 50)
        myFont3 = ImageFont.truetype('./Assets/fonts/DrumNBass-ywGy2.ttf', 80)
        draw.text((60,270),membername,font = myFont,fill = (0,0,0))
        draw.text((110,400),joined_at,font = myFont2,fill = (0,0,0))
        draw.text((60,580),to,font = myFont3,fill = (255,255,255), stroke_width=3, stroke_fill=(0,0,0))
        wchannel = get(member.guild.channels, id=channelid[0])

        embed = discord.Embed(description = f"{member.display_name}** Welcome to {member.guild.name.title()} !!** \n Why not start with introducing yourself in Chats!",color = random.choice(self.colors))
        
        with BytesIO() as a:
            welcome.save(a, 'PNG')
            a.seek(0)
            embed.set_image(url="attachment://profile.png")
            await wchannel.send(content = member.mention,file = discord.File(a, filename = "profile.png"),embed = embed)

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        if not isinstance(error, commands.CommandOnCooldown):
            try:
                ctx.command.reset_cooldown(ctx)
            except:
                pass
        if isinstance(error ,commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(description = "You do not have the required Permissions to Use this command\nContact the Admin/Mods for the following",color=0xe74c3c),delete_after = 10)
            await ctx.message.delete() 
        elif isinstance(error ,commands.errors.NotOwner):
            em = discord.Embed(title ="You Do Not own this Bot!! ",description =f"Ask the Bot Owner for More info - {str(self.bot.get_user(self.bot.owner_id))}",color = 0xe74c3c)
            await ctx.send(embed = em,delete_after = 8)
        elif isinstance(error,commands.errors.ChannelNotFound):
            await ctx.send(embed = discord.Embed(title = "Channe not found!",description = "No such Text Channel exists\nPlease Type #channel_name to Mention a Channel",color = 0xe74c3c))
        elif isinstance(error ,commands.MissingRequiredArgument):
            em = discord.Embed(description =f"You are missing one necessary parameter that is **{error.param.name}** \nType `{prefix}help command_name` for more info",color = 0xe74c3c)
            await ctx.send(embed = em,delete_after = 8)
        elif isinstance(error , commands.errors.MemberNotFound):
            await ctx.send(embed = discord.Embed(description="Member not found!!",color= 0xe74c3c,delete_after = 4))
            await ctx.message.delete()
        elif isinstance(error , commands.errors.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            msg = revert(error.retry_after)
            embed = discord.Embed(title = "Cooldown", description = str(msg), color = 16580705)
            embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            embed.set_thumbnail(url = 'https://cdn.pixabay.com/photo/2012/04/13/00/22/red-31226_640.png')
            await ctx.send(embed = embed ,delete_after = 5)
            await ctx.message.delete()
        else:

            await ctx.message.clear_reactions()
            await ctx.send(embed = discord.Embed(description = "An unknown error occured and my developer has been notified about it.",color= 0x8DDFE3))

            try:

                errno = "".join(traceback.format_exception(type(error), error, error.__traceback__))

                embed = discord.Embed(title = f"Command: {ctx.command.name}", description = f"`*3py\n{errno}\n`*3", color = 0xe74c3c)
                embed.add_field(name = "Message ID", value = f"[Click Here]({ctx.message.jump_url})", inline = False)
                embed.add_field(name = "Author", value = ctx.author.mention)
                owner = await self.bot.fetch_user(self.bot.owner_id)
                await owner.send(embed = embed)
                

            except Exception:
                raise Exception
        
        
    @commands.Cog.listener()
    async def on_message(self,message):

        user_id = self.bot.user.id
        if message.guild is None:
            return
        ai_id = await self.bot.pg_con.fetchrow("SELECT aichannel FROM guild WHERE guildid = $1",message.guild.id)
        
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick = remove(message.author.display_name))
            except:
                pass
            await message.channel.send(f'Welcome back {message.author.name}, I removed you AFK')

        for id, reason in afks.items():
            member = get(message.guild.members, id = id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                await message.reply(f"{member.name} is AFK ; AFK note : {reason}")

        if ai_id != None:
            ai_id = ai_id[0]
            if message.channel.id == ai_id:
                if not message.author.bot:
                    for i in toxic:
                        if i in message.content:    
                            await message.reply("don't talk toxic for god's sake -_-")
                            return
                    if "@" in str(message.content):    
                        await message.reply("don't ping tbh.....")
                    else:
                        listtrainer.train([message.content])
                        await self.append(message.content)
                        await message.reply(chatbot.get_response(message.content))
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",message.guild.id)
        if message.content in (f"<@{user_id}>", f"<@!{user_id}>"):
            return await message.reply(
                "My prefix here is `{}`".format(prefix[0])
            )
        
        
        

def setup(bot):
    bot.add_cog(Events(bot))

