import datetime
import discord
from discord.ext import commands
import random
from PIL import Image,ImageFont,ImageDraw,ImageChops
import requests
from afks import afks
from io import BytesIO


urls = {"demonslayer":"https://wallpapercave.com/wp/wp5486939.jpg",
        "warzone":"https://wallpaperaccess.com/full/930562.jpg",
        "maskcodes":"https://www.zastavki.com/pictures/1280x720/2019Creative_Wallpaper_Gas_mask_with_a_numerical_code_background_136603_26.jpg",
        "mikasa":"https://images.wallpapersden.com/image/download/anime-shingeki-no-kyojin-mikasa-ackerman_ZmZna26UmZqaraWkpJRmZ21lrWxnZQ.jpg",
        "devilmay":"https://images.wallpapersden.com/image/download/devil-may-cry-5-4k_a2hubWyUmZqaraWkpJRmZ21lrWxnZQ.jpg",
        "binary":"https://images.wallpaperscraft.com/image/code_coding_binary_code_abstract_patterns_112140_1280x720.jpg",
        "default":"https://images.hdqwalls.com/download/anime-sunset-scene-b8-1280x720.jpg",
        "blocks":"https://cdn.wallpapersafari.com/77/30/wKc3Jy.jpg",
        "pubg":"https://hdqwalls.com/download/pubg-android-game-4k-eh-1280x720.jpg",
        "naruto":"https://images.hdqwalls.com/download/kakashi-hatake-anime-4k-yk-1280x720.jpg"}



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

class Information(commands.Cog):
    """Information commands regarding leaderboard, server, Image profile"""
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors
        

    
    async def add(self,id,amount = 2000):
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE userid = $1",id)
        await self.bot.pg_con.execute("UPDATE users SET credits = $1 WHERE userid = $2",user[1]+amount,id)

    async def get(self,id):
        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE userid = $1",id)
        if user is None:
            return None
        return user[1]

    async def check(self,id):
        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE userid = $1",id)
        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (userid, credits,bg) VALUES ($1,$2,$3)",id,2000,['default'])
            
    async def available(self,id):
        urls = await self.bot.pg_con.fetchrow("SELECT bg FROM users WHERE userid = $1",id)
        if urls is None:
            await self.bot.pg_con.execute("UPDATE users SET bg = $1 WHERE userid = $2",['default'],id)
            return ['default']
        return urls[0]

    async def update(self,id,back):
        urls = await self.available(id)
        if urls is None:
            urls = []
        if back in urls:   
            urls.remove(back)
        urls.insert(0,back)
        await self.bot.pg_con.execute("UPDATE users SET bg = $1 WHERE userid = $2",urls,id)
    
    async def top(self):
        tops = await self.bot.pg_con.fetch("SELECT * FROM users ORDER BY credits DESC NULLS LAST")
        top = {}
        for i in tops:
            top[i[0]] = i[1]
        return top

    
    @commands.command()
    async def afk(self,ctx,*,reason ="No reason provided"):
        """Go AFK (away from keyboard) for some time being"""
        member = ctx.author
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick = f"(AFK) {member.display_name}")
            except:
                pass
        afks[member.id] = reason
        embed = discord.Embed(title = ":zzz: Member AFK", description = f"{member.mention} has gone AFK",color = member.color)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name='AFK note: ',value=reason)
        await ctx.send(embed=embed)

    @commands.command(aliases = ['lb'])
    async def leaderboard(self,ctx):
        """Check your position in the Global leaderboard of Doppleganger"""
        tops = await self.top()
        bg = Image.open("./Assets/images/lb.png")
        myFont = ImageFont.truetype('./Assets/fonts/Roboto-Regular.ttf', 60)
        myFont2 = ImageFont.truetype('./Assets/fonts/Roboto-Regular.ttf', 50)
        x = 10
        if len(tops)<10:
            x = len(tops)
        em = discord.Embed(title = f"Global LeaderBoard of DoppleGanger",color = random.choice(self.colors))
        index = 1
        x,y = 17,180
        x1 = 180
        x2 = 860
        draw = ImageDraw.Draw(bg)
        for id,credits in tops.items():
            member= self.bot.get_user(id)
            if member is None:
                continue
            if member.bot:
                continue 
            name = str(member)
            if len(name)>19:
                name = f"{name[:19]}.."
            draw.text((x,y),f"#{index}",font = myFont,fill = (255,255,255))  
            draw.text((x1,y),name,font = myFont,fill = (255,255,255))   
            draw.text((x2,y),str(credits),font = myFont2,fill = (255,255,255))   
            y+=140
            if index == x:
                break
            else:
                index +=1

        
        with BytesIO() as a:
            bg.save(a, 'PNG')
            a.seek(0)
            em.set_image(url="attachment://leader.png")
            em.set_footer(text = "Type locallb or localleaderboard to Get your server's Leaderboard")
            await ctx.send(file = discord.File(a, filename = "leader.png"),embed = em)

    @commands.command(aliases = ['localleaderboard'])
    async def locallb(self,ctx):
        """See your stand in your specific guild"""
        tops = await self.top()
        bg = Image.open("./Assets/images/lb2.png")
        myFont = ImageFont.truetype('./Assets/fonts/Roboto-Regular.ttf', 25)
        myFont2 = ImageFont.truetype('./Assets/fonts/Roboto-Regular.ttf', 20)
        
        x = 10
        if len(tops)<10:
            x = len(tops)
        em = discord.Embed(title = f"{ctx.guild.name}'s Leaderboard",color = random.choice(self.colors),timestamp = datetime.datetime.utcnow())
        draw = ImageDraw.Draw(bg)
        datas = {}
        for i in ctx.guild.members:
            credit = await self.get(i.id)
            if credit is not None:
                datas[credit] = i.id
        
        newdata = sorted(datas.items(),reverse=True)

        index = 1
        x,y = 10,67
        x1 = 70
        x2 = 380

        for i in newdata:
            member= self.bot.get_user(i[1])
            name = str(member)
            if member.bot:
                continue 
            if len(name)>19:
                name = f"{name[:19]}.."
            draw.text((x,y),f"#{index}",font = myFont,fill = (0,0,0))  
            draw.text((x1,y),name,font = myFont,fill = (0,0,0))   
            draw.text((x2,y),str(i[0]),font = myFont2,fill = (0,0,0))   
            y+=51
            if index == x:
                break
            else:
                index +=1
        
        
        with BytesIO() as a:
            bg.save(a, 'PNG')
            a.seek(0)
            em.set_image(url="attachment://leader2.png")
            em.set_footer(text = "Type lb or leaderboard to Get Global Leaderboard")
            await ctx.send(file = discord.File(a, filename = "leader2.png"),embed = em)

    @commands.command(aliases = ['switch','swap'])
    async def setbg(self,ctx,back):
        """Set background for your profile"""
        back = back.lower()
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        urlname = await self.available(ctx.author.id)
        if back in urls.keys():
            if back in urlname:
                
                await self.update(ctx.author.id,back)
                await ctx.send("Done :)")
            else:
                await ctx.send(embed = discord.Embed(description = f"You don't have `{back}` background\nType `{prefix}shop` for more info",color = random.choice(self.colors)),delete_after = 10)
        else:
            await ctx.send(embed = discord.Embed(description = f"Is there any such Background available, I doubt there is, Please recheck the name\nType `{prefix}shop` for more info",color = random.choice(self.colors)),delete_after = 10)


    @commands.command(aliases = ["background","backs",'back'])
    async def backgrounds(self,ctx):
        """See all the available backgrounds for your profile"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        backgrounds = await self.available(ctx.author.id)
        names = " , ".join(backgrounds)
        embed = discord.Embed(title = "Backgrounds Available for profile : ",description = names)
        embed.add_field(name = "Active Background : ",value=backgrounds[0],inline=False)
        embed.add_field(name = "Switch Help : ",value= f"Type `{prefix}setbg + bg_name` or `{prefix}switch + bg_name` to change background",inline=False)
        counter = 1
        await ctx.send(embed = embed)

        for i in backgrounds:
            await ctx.send(f"{counter}) {i}\n{urls[i]}")
            counter+=1  
            



    @commands.command(aliases = ['si'])
    async def serverinfo(self,ctx, guild = discord.Guild):
        """What is the stand of your server? have a look at that"""
        guild = ctx.guild
        embed = discord.Embed(title = f'ID: {guild.id}', color = random.choice(self.colors))
        embed.add_field(name = "Verification Level", value = guild.verification_level, inline = False)
        embed.add_field(name = "Region", value = guild.region)
        embed.add_field(name = "Members", value = guild.member_count)
        embed.add_field(name = "Server Owner", value = f"{guild.owner} [{guild.owner_id}]", inline = False)
        embed.add_field(name = "Created On", value = guild.created_at.__format__('%A, %B %d %Y @ %X %p'), inline = False)
        embed.add_field(name = "Channels", value = len(guild.text_channels))
        embed.set_thumbnail(url = guild.icon_url)
        embed.set_author(icon_url = guild.icon_url, name = guild.name)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['pfp'])
    async def profilepic(self,ctx,member:discord.Member = None):
        """Get a enlarged image of your profile"""
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=member.name.title(),timestamp = datetime.datetime.utcnow(),color = member.color)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed = embed)

        
    @commands.command(aliases=["whois"])
    async def profile(self,ctx, *, member: discord.Member = None):
        """Get an Image UI Profile of yourself"""
        if member==None:
            member = ctx.author   
        await self.check(member.id)
        created_at = member.created_at.strftime('%a, %#d \n%B %Y')
        joined_at = member.joined_at.strftime('%a, %#d \n%B %Y')
        credits = await self.get(member.id)
        top_role = member.top_role.name
        ava = await self.available(member.id)
        status = str(member.status).upper()
        url = urls[ava[0]]
        background =Image.open(requests.get(url, stream=True).raw)
        
        
        asset = member.avatar_url_as(size = 256)
        guildemote = member.guild.icon_url_as(size = 256)
        data = BytesIO(await asset.read())
        gdata = BytesIO(await guildemote.read())
        pfp = Image.open(data).convert("RGB")
        logo = Image.open(gdata).convert("RGB")
        pfp = circle(pfp,(255,255))
        logo = circle(logo,(180,180))

        name = str(member)
        if len(top_role)>12:
            top_role = top_role[:13]
        if len(name) > 20:
            name = name[:21]
            
        background =Image.open(requests.get(url, stream=True).raw)
        main = Image.open("./Assets/images/pro.png")
        bg = Image.new('RGBA', (1280,720), (0, 0, 0, 0))
        bg.paste(background, (0,0))
        bg.paste(main, (0,0), mask=main)
        draw = ImageDraw.Draw(bg)
        myFont = ImageFont.truetype('./Assets/fonts/DrumNBass-ywGy2.ttf', 45)
        draw.text((570,270),name,font = myFont,fill = (0,0,0), stroke_width=3, stroke_fill=(255,255,255))
        myFont = ImageFont.truetype('./Assets/fonts/DrumNBass-ywGy2.ttf', 35)
        myFont2 = ImageFont.truetype('./Assets/fonts/DrumNBass-ywGy2.ttf', 30)
        myFont3 = ImageFont.truetype('./Assets/fonts/DrumNBass-ywGy2.ttf', 25)
        draw.text((850,550),created_at,font = myFont2,fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))
        draw.text((850,425),joined_at,font = myFont2,fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))
        draw.text((150,555),str(credits),font = myFont,fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))
        draw.text((122,435),str(member.id),font = myFont3,fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))
        draw.text((500,555),top_role,font = myFont,fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))
        draw.text((500,425),status,font = myFont,fill = (0,0,0), stroke_width=2, stroke_fill=(255,255,255))   
        bg.paste(pfp, (275, 102), pfp)
        bg.paste(logo, (25, 25), logo)
        with BytesIO() as a:
            bg.save(a, 'PNG')
            a.seek(0)
            await ctx.send(file = discord.File(a, filename = "e.png"))
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",member.guild.id)
        prefix = prefix[0]
        if ava[0] =="default":
            await ctx.send(f"{member.mention} can Also Buy/Set Different BackGround from the Default one\nType `{prefix}shop` to see the Background images list and `{prefix}swap + imgname` to change the background")
   
   
def setup(bot):
    bot.add_cog(Information(bot))
