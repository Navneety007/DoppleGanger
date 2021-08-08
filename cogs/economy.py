import discord
from discord.ext import commands,tasks
import random
from discord.ext.commands.core import command
from discord.utils import get  
import datetime
import asyncio



less = discord.Embed(title="Failed !",description = f"You don't have sufficient Credits :( ",color = discord.Colour.red())
type = discord.Embed(title="Invalid Unit !",description = f"Amount should be an integer ",color = discord.Colour.red())
amount = discord.Embed(title = "Amount Missing!", description = "Please enter the amount to be used !",color = discord.Colour.red())      

names = ['Jenny','Lauren','Humble','Dan','Matthew','Blacksmith','Clarke','Simon','Christian','Hector','Albert','Vader','Walker','Phillip']
shopping = [{"name":"demonslayer","price" : 120000 , "description" : "`.setbg demonslayer` Click [HERE](https://wallpapercave.com/wp/wp5486939.jpg) for Image Preview" } ,
            {"name":"warzone","price" : 100000 , "description" : "`.setbg warzone` Click [HERE](https://wallpaperaccess.com/full/930562.jpg) for Image Preview" } ,
            {"name":"maskcodes","price" : 20000 , "description" : "`.setbg maskcodes` Click [HERE](https://www.zastavki.com/pictures/1280x720/2019Creative_Wallpaper_Gas_mask_with_a_numerical_code_background_136603_26.jpg) for Image Preview" },
            {"name":"mikasa","price" : 199999 , "description" : "`.setbg mikasa` Click [HERE](https://images.wallpapersden.com/image/download/anime-shingeki-no-kyojin-mikasa-ackerman_ZmZna26UmZqaraWkpJRmZ21lrWxnZQ.jpg) for Image Preview" } ,
            {"name":"devilmay","price" : 40000 , "description" : "`.setbg devilmay` Click [HERE](https://images.wallpapersden.com/image/download/devil-may-cry-5-4k_a2hubWyUmZqaraWkpJRmZ21lrWxnZQ.jpg) for Image Preview" } ,
            {"name":"binary","price" : 100000 , "description" : "`.setbg binary` Click [HERE](https://images.wallpaperscraft.com/image/code_coding_binary_code_abstract_patterns_112140_1280x720.jpg) for Image Preview" },
            {"name":"naruto","price" : 80000 , "description" : "`.setbg naruto` Click [HERE](https://images.hdqwalls.com/download/kakashi-hatake-anime-4k-yk-1280x720.jpg) for Image Preview" },
            {"name":"pubg","price" : 30000 , "description" : "`.setbg pubg` Click [HERE](https://hdqwalls.com/download/pubg-android-game-4k-eh-1280x720.jpg) for Image Preview" },
            {"name":"blocks","price" : 5000 , "description" : "`.setbg blocks` Click [HERE](https://cdn.wallpapersafari.com/77/30/wKc3Jy.jpg) for Image Preview" } ]

huntanimals = [':hamster:',':rabbit:',':fox:',':bear:',':chicken:',':baby_chick:',':hatching_chick:',0]
fishcate = [':fish:',':tropical_fish:',':blowfish:',0,':octopus:',':squid:',':dolphin:',':shark:']
stuff = [':bouquet:',':ear_of_rice:',':potted_plant:',':tulip:',':rose:',':hibiscus:',':cherry_blossom:',':blossom:',':sunflower:',':shell:']
randomitem = [':soccer:',':boomerang:',':yo_yo:',':badminton:',':lacrosse:',':roller_skate:',':musical_keyboard:',':video_game:',':dart:',':jigsaw:',':violin:',':microphone:',':trophy:',':video_camera:',':film_frames:',':fire_extinguisher:',':syringe:',':magic_wand:',':pill:',':sewing_needle:']


class Economy(commands.Cog):
    """Economy system (Currency : **credits**) envolving irl commands"""
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

    async def sub(self,id,name):
        data = await self.bot.pg_con.fetchrow("SELECT inventory FROM users WHERE userid = $1",id)
        data = list(data[0])
        data.remove(name)
        await self.bot.pg_con.execute("UPDATE users SET inventory = $1 WHERE userid = $2 ",data,id)

    async def plus(self,id,name):
        data = await self.bot.pg_con.fetchrow("SELECT inventory FROM users WHERE userid = $1",id)
        data = data[0]
        if data is None:
            data = []
        data.insert(0,name)
        await self.bot.pg_con.execute("UPDATE users SET inventory = $1 WHERE userid = $2 ",data,id)

    async def invent(self,id):
        inventory = await self.bot.pg_con.fetchrow("SELECT inventory FROM users WHERE userid = $1",id)
        return inventory[0]

    
    async def available(self,id):
        urls = await self.bot.pg_con.fetchrow("SELECT bg FROM users WHERE userid = $1",id)
        return urls[0]

    async def update(self,id,List):
        await self.bot.pg_con.execute("UPDATE users SET bg = $1 WHERE userid = $2",List,id)


    @commands.command()
    async def donate(self,ctx,member:discord.Member,amount = None):
        """Donate a member some amount from your credits"""
        if member==ctx.author or member.bot:
            return await ctx.send("You can't donate money to a bot or yourself -_-")
        await self.check(ctx.author.id)
        await self.check(member.id)
        if amount == None:
            await ctx.send(embed = amount)
            return
        try:
            amount = int(amount)
            amount = abs(amount)
        except:
            await ctx.send(embed = type)

        if await self.get(ctx.author.id)>= amount:
            await self.add(ctx.author.id,-1*amount)
            await self.add(member.id,amount)            
            embed = discord.Embed(title="Credits Transfered",description = f"{ctx.author.name} Have donated {amount} to {member.mention}",color = random.choice(self.colors))
            await ctx.send(embed = embed)
        else:
            await ctx.send(embed = less)


    @commands.command()
    @commands.is_owner()
    async def reward(self,ctx,member:discord.Member,amount:int = 10000):
        em = discord.Embed(title = f"Congratulations {member.name} !!! ",description = f"{member.mention} is rewarded {amount} credits ",color = random.choice(self.colors))
        em.timestamp = datetime.datetime.utcnow()
        em.set_thumbnail(url = self.bot.user.avatar_url)
        await ctx.send(embed = em)
        await self.check(member.id)
        await self.add(member.id,amount)
 
    @commands.command(aliases = ['bet'])
    async def gamble(self,ctx,amount):
        """Gamble money and get return from 50-100%"""
        await self.check(ctx.author.id)
        try:
            amount = int(amount)
            amount = abs(amount)
        except:
            await ctx.send(embed = type,delete_after =10)
            return
        if amount>await self.get(ctx.author.id):
            await ctx.send(embed = less)
            return
        if amount == 0:
            await ctx.send(embed = discord.Embed(title = "Huh",description = "Amount can't be Zero :D ",color = discord.Colour.red(),delete_after = 10))
            return

        mystrike = random.randint(1,12)
        botstrike = random.randint(2,12)
        if mystrike>botstrike:
            percent = random.randint(50,100)
            amount_add = int(amount*(percent/100))
            await self.add(ctx.author.id,amount_add)
            credits = await self.get(ctx.author.id)
            embed = discord.Embed(description = f"""You Won **{amount_add} credits**

Percent Won: **{percent}%**

**New Balance:** {credits}
""",color = random.choice(self.colors))
    
            embed.set_author(name =f"Woow Seems like {ctx.author.name} plays well",icon_url=ctx.author.avatar_url)
            embed.add_field(name = f"**{ctx.author.name.title()}** ",value=f"Strikes `{mystrike}`")
            embed.add_field(name = f"**{self.bot.user.name.title()}** ",value=f"Strikes `{botstrike}`")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url = self.bot.user.avatar_url)

            await ctx.send(embed = embed)
        elif mystrike<botstrike:
            percent = random.randint(0,80)
            lost = int(amount*(percent/100))
            await self.add(ctx.author.id,-1*lost)
            credits = await self.get(ctx.author.id)
            embed = discord.Embed(description = f"""You Lost **{lost} credits**

Percent Lost: **{percent}%**

New Balance: **{credits}**
""",color = random.choice(self.colors))
            embed.set_author(name = f"Crap Play {ctx.author.name} !",icon_url=ctx.author.avatar_url)
            embed.add_field(name = f"**{ctx.author.name.title()}** ",value=f"Strikes `{mystrike}`")
            embed.add_field(name = f"**{self.bot.user.name.title()}** ",value=f"Strikes `{botstrike}`")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url = self.bot.user.avatar_url)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(description = f"""**It was a TIE**
            
""",color = random.choice(self.colors))
            embed.set_author(name = f"Tie",icon_url=ctx.author.avatar_url)
            embed.add_field(name = f"**{ctx.author.name.title()}** ",value=f"Strikes `{mystrike}`")
            embed.add_field(name = f"**{self.bot.user.name.title()}** ",value=f"Strikes `{botstrike}`")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url = self.bot.user.avatar_url)

            await ctx.send(embed = embed)


    @commands.command()
    async def earn(self,ctx):
        """Get a list of all the ways to earn"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        em = discord.Embed(title = "Ways To Earn : ",color = random.choice(self.colors))
        em.add_field(name = f"Work `{prefix}work`",value = f"Work in every 60 mins to get random money acc. to your credits")
        em.add_field(name = f"Slots `{prefix}slots`",value = f"Bet to Have quadruple return if won and Loose the money if lost")        
        em.add_field(name = f"Gamble `{prefix}gamble`",value = f"Gambleto Win from 50% to 100% and loose between 0% to 100%")
        em.add_field(name = f"Hunt `{prefix}hunt`",value = f"Hunt animals To sell them for credits")
        em.add_field(name = f"fish `{prefix}fish`",value = f"Catch Aquatic animals and sell them for credits")
        em.add_field(name = f"Sell `{prefix}sell`",value = f"Sell Items from your inventory to earn Credits")
        em.add_field(name = f"Beg `{prefix}Beg`",value = f"Beg in every 25 mins,And get Credits from 1 to 10000")
        em.add_field(name = f"Time",value = f"Get money in every 24 hours according to Your Server")
        em.add_field(name = f"Donation `{prefix}donate + @membername + amount`",value = "Donate Money to others and get money donated")
        em.set_footer(text = f"Join our Main server for instant 10000 credits and extra benefits ,Type {prefix}join  ")
        em.set_author(name = self.bot.user.name,icon_url=self.bot.user.avatar_url)
        em.set_thumbnail(url = self.bot.user.avatar_url)
        await ctx.send(embed = em)
        
    
    @commands.command(aliases = ['earn_credits'])
    @commands.cooldown(1, 3600 , type = commands.BucketType.user)
    async def work(self,ctx):
        """Work in every 1 hr to earn money"""
        await self.check(ctx.author.id)
        coder = get(ctx.author.guild.roles, id=780280968183152701)
        gamer = get(ctx.author.guild.roles, id=798537784348114955)
        anime_weeb = get(ctx.author.guild.roles, id=798538056814297110)
        roles = [coder,gamer,anime_weeb]
        no_ = 1
        for i in roles:
            if i in ctx.author.roles:
                no_+=1
                
        credits = random.randint(500,600*no_)
        
        await self.add(ctx.author.id,int(credits))
        money = await self.get(ctx.author.id)
        em = discord.Embed(title ="Work Results : ",description = f"{ctx.author.mention} has Earned {credits} Credits through Work :)\nTotal Credits : {money}",color = random.choice(self.colors))
        em.set_author(name = self.bot.user.name,url = self.bot.user.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)


    
    @commands.Cog.listener()
    async def on_ready(self):  
        yo = "haha"
        #await self.picking.start()

    
    @tasks.loop(seconds=4000)
    async def picking(self):
        channel = self.bot.get_channel(779743465252192297)
        amount = random.randint(20,200)
        thing = random.choice(randomitem)
        def check(message):
            return message.content.lower() == "pick"

        embed = discord.Embed(title = f"Someone Dropped their {thing} {thing.replace(':','')} and some Credits",description = "Type `pick` to Add it to you inventory and then sell it for Credits", color=random.choice(self.colors))
        embed.timestamp = datetime.datetime.utcnow()
        msg = await channel.send(embed = embed)
        try:
            authormsg = await self.bot.wait_for('message', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
            
        else:
            author = authormsg.author
            await self.check(author.id)
            await channel.send(embed=discord.Embed(description=f"{author.name} Got {thing} {thing.replace(':','')} and {amount} Credits", color=random.choice(self.colors)))
            await self.add(author.id,amount)
            await self.plus(author.id,thing)

    @commands.command(aliases = ["credit"])
    async def credits(self,ctx):
        """Check your credits balance"""
        await self.check(ctx.author.id)
        credits =  await self.get(ctx.author.id)
        em = discord.Embed(title = "Credits Info : ",color = random.choice(self.colors))
        em.set_thumbnail(url = ctx.author.avatar_url)
        em.add_field(name = f"Credits of {ctx.author.name} -",value = credits,inline = False)
        em.add_field(name ="Roles - ",value=" ".join([role.mention for role in ctx.author.roles]),inline = False)
        em.set_author(name = self.bot.user.name,url = self.bot.user.avatar_url)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)

    @commands.command(aliases = ["slot"])
    @commands.cooldown(1, 900 , type = commands.BucketType.user)
    async def slots(self,ctx,amount = None):
        """Put money on bet in slots and get 4 times return if won"""
        await self.check(ctx.author.id)

        if amount == None:
            await ctx.send(embed = amount)
            return
        try:
            amount = int(amount)
            amount = abs(amount)
        except:
            await ctx.send(embed = type,delete_after = 12)

        final = []

        if await self.get(ctx.author.id)>= amount:
            for i in range(3):
                a = random.choice([":coin:",":money_mouth:",":money_with_wings:"])

                final.append(a)

            await ctx.send("   ".join(final))
            if final[0]==final[1]==final[2]:
                await self.add(ctx.author.id,amount*4)
                credits = await self.get(ctx.author.id)
                em = discord.Embed(title = "Voilaa !!" , description = f"{ctx.author.mention} have got {amount}x4 credits By Slots :) \nTotal Credits : {credits}",color = random.choice(self.colors))
                
            else:
                await self.add(ctx.author.id,-1*amount) 
                credits = await self.get(ctx.author.id)
                em = discord.Embed(title = "Oppsie !!" , description = f"{ctx.author.mention} have Lost {amount} credits \nBetter luck Next time :(\nTotal Credits : {credits}",color = random.choice(self.colors))
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url = ctx.author.avatar_url)
            await ctx.send(embed = em)
        else:
            await ctx.send(embed = less,delete_after = 12)


    @commands.command()
    async def shop(self, ctx):
        """Check the shop for all the available items to buy"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        em = discord.Embed(title = "Buy Items",description = "Type `.buy + itemname` to buy an Item",color = random.choice(self.colors))
        for item in shopping:
            name = item['name'].title()
            price = item['price']
            description = item['description']
            em.add_field(name = name,value = f"Price : {price} \nDescription : {description}")
        em.add_field(name = "Thank Someone",value="Say `.thank @membername` to donate him\her 200 credits ")
        em.set_footer(text=f"Join Our main Server and Get extra 10000 credits. Type {prefix}invite")
        em.set_author(name = self.bot.user.name,icon_url=self.bot.user.avatar_url)
        await ctx.send(embed = em)
       
    @commands.command()
    @commands.cooldown(1, 1000 , type = commands.BucketType.user)
    async def beg(self,ctx):
        """Beg for credits and items"""
        await self.check(ctx.author.id)
        
        mystuff = random.choice(stuff)
        money = [0,0,random.randint(10,2000),random.randint(30,500),random.randint(100,200),random.randint(1,2500),random.randint(2,300)]
        amount = random.choice(money)
        person = random.choice(names)
        await self.add(ctx.author.id,amount)
        ranstuff = f"{mystuff} {mystuff.replace(':','')}"
        if amount == 0:
            await ctx.send("Ahh , You got Nothing !! Such a Shame :(")
        elif amount>1000:
            await ctx.send(embed = discord.Embed(title = "Woow!!",description = f"Seems like {person.title()} donated you {amount} and {ranstuff} :star_struck: !! ",color = random.choice(self.colors)))
        elif amount <500 and amount >100:
            await ctx.send(embed = discord.Embed(title = "Nice!!",description = f"You got mediocre amount of {amount} and a {ranstuff} from {person.title()} :) !! ",color = random.choice(self.colors)))
        elif amount <100:
            await ctx.send(embed = discord.Embed(title = "Ahhh!",description = f"{person.title()} donated you a small portion of {amount} and a {ranstuff} :expressionless: !! ",color = random.choice(self.colors)))
        await self.plus(ctx.author.id,mystuff)

    @commands.command(aliases = ['inven','inv'])
    async def inventory(self,ctx,member:discord.Member = None):
        """Check your inventory ~~and flex~~"""
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]

        if member == None:
            member = ctx.author
        await self.check(member.id)
        
        data = await self.invent(member.id)
        
        embed = discord.Embed(title = "Inventory",description = f"Join our main server to get instant 10k credits. Type `{prefix}join`",color = random.choice(self.colors))
        if data is not None:

            misc = set()
            fishes = set()
            animals = set()
            no = set()

            for i in fishcate:
                if i in data:
                    fishes.add(f"**{data.count(i)}** x {i}")
            for i in huntanimals:
                if i in data:
                    animals.add(f"**{data.count(i)}** x {i}")
            for i in randomitem:
                if i in data:
                    no.add(f"**{data.count(i)}** x {i}")
            for i in stuff:
                if i in data:
                    misc.add(f"**{data.count(i)}** x {i}")
            
                    
            if len(animals)>0:
                items = " | ".join(animals)
                embed.add_field(name = "Animals ",value= items,inline=False)
            if len(fishes)>0:
                items = " | ".join(fishes)
                embed.add_field(name = "Fishes ",value= items,inline=False)
            if len(no)>0:
                my = " | ".join(no)
                embed.add_field(name = "Items ",value= my,inline=False)
            if len(misc)>0:
                items = " | ".join(misc)
                embed.add_field(name = "Miscellaneous ",value= items,inline=False)
        else:
            embed.add_field(name = "Items",value= "You got nothing in your inventory]")
            
        credits = await self.get(member.id)
        embed.add_field(name="Credits",value = credits,inline=False)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text = f"Type {prefix}sell + Item_name(click to know the name) to sell it for credits")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['sells'])
    async def sell(self,ctx,item):
        """Sell item(s) from your inventory to earn money"""
        inventory = await self.invent(ctx.author.id)
        await self.check(ctx.author.id)
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❎"]
        name = random.choice(names)
        if item.lower() == "all":
            items = len(inventory)
            if not items == 0:
                amount = random.randrange(items*250,items*600)
                msg1 = discord.Embed(title = "Offer",description = f"{name} is offering you {amount} for All your Items",color = random.choice(self.colors))
                msg1.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                msg1.set_author(name = f"Offer for {ctx.author.name}",icon_url=ctx.author.avatar_url)
                msg1.set_thumbnail(url="https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhouette.png")
                msg1 = await ctx.send(embed = msg1)
                await msg1.add_reaction("✅")
                await msg1.add_reaction("❎")
                try:
                    reaction = await self.bot.wait_for('reaction_add',timeout = 20.0,check = check)
                except asyncio.TimeoutError:
                    msg2 = discord.Embed(title = "Offer Decliend",description = f"{ctx.author.mention} didn't react in time , So the offer was declined",color =  discord.Colour.red())
                    msg2.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                    await msg1.edit(embed = msg2)
                    return
                else:
                    if reaction[0].emoji == "✅":
                        latest = await self.invent(ctx.author.id)
                        if latest == inventory:
                            await self.add(ctx.author.id,amount)
                            msg2 = discord.Embed(title = "Offer Accepted",description = f"{ctx.author.mention} Sold All of his/her items for {amount} to {name}",color = discord.Colour.green())
                            msg2.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                            msg2.set_thumbnail(url="https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhouette.png")
                            
                            for i in inventory:
                                await self.sub(ctx.author.id,i)
                        else:
                            msg2 = discord.Embed(title = "what was that",description = f"Some items were Sold or gained in between the Process of trading !! , pls try again :(",color = discord.Colour.green())
                            msg2.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                            msg2.set_thumbnail(url="https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhouette.png")
                             
                    else:
                        msg2 = discord.Embed(title = "Offer Declined",description = f"{ctx.author.mention} Declined the Offer",color =  discord.Colour.red())
                        msg2.timestamp = datetime.datetime.utcnow()
                    await msg1.edit(embed = msg2)
                    return
            else:
                await ctx.send("You have nothing in your inventory")
                return

        item = f':{item.lower()}:'
        amount = 0 
        if item in stuff:
            amount = random.randint(200,400)
        elif item in huntanimals:
            amount = random.randint(400,600)
        elif item in fishcate:
            amount = random.randint(300,500)
        elif item in randomitem:
            amount = random.randint(250,550)
        else:
            await ctx.send(embed = discord.Embed(title = "Was that a Typo",description = f"Probably you mispelled {item.replace9(':','')} \nYou can go to your inventory (`.inven`) and click the item to know it's name",color = discord.Colour.red()))
        
        
        if item in inventory:
            
            msg1 = discord.Embed(title = "Offer",description = f"{name} is offering you {amount} for {item} {item.replace(':','')}",color = random.choice(self.colors))
            msg1.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
            msg1.set_author(name = f"Offer for {ctx.author.name}",icon_url=ctx.author.avatar_url)
            msg1.set_thumbnail(url="https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhouette.png")
            msg1 = await ctx.send(embed = msg1)
            await msg1.add_reaction("✅")
            await msg1.add_reaction("❎")
            try:
                reaction = await self.bot.wait_for('reaction_add',timeout = 60.0,check = check)
            except asyncio.TimeoutError:
                msg2 = discord.Embed(title = "Offer Decliend",description = f"{ctx.author.mention} didn't react in time , So the offer was declined",color =  discord.Colour.red())
                msg2.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                await msg1.edit(embed = msg2)
                return
            else:
                if reaction[0].emoji == "✅":
                    if item in inventory:
                        await self.add(ctx.author.id,amount)
                        msg2 = discord.Embed(title = "Offer Accepted",description = f"{ctx.author.mention} Sold {item} {item.replace(':','')} for {amount} to {name}",color = discord.Colour.green())
                        msg2.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                        msg2.set_thumbnail(url="https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhouette.png")
                        await self.sub(ctx.author.id,item)
                    else:
                        msg2 = discord.Embed(title = "Ahhh..",description = f"{item} {item.replace(':','')} is no longer available in {ctx.author}'s Inventory",color = discord.Colour.green())
                        msg2.set_footer(text = "Rates of Items Keeps on Fluctuating, You can Decline and maybe Try again Later")
                        msg2.set_thumbnail(url="https://www.clipartkey.com/mpngs/m/126-1261730_suit-clipart-anonymous-anonymous-person-silhouette.png")
                        
                else:
                    msg2 = discord.Embed(title = "Offer Declined",description = f"{ctx.author.mention} Declined the Offer",color =  discord.Colour.red())
                    msg2.timestamp = datetime.datetime.utcnow()
                await msg1.edit(embed = msg2)
    @commands.command()
    async def buy(self,ctx,*,item):
        """Buy items available in shop"""
        item = item.lower()
        prefix = await self.bot.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await self.check(ctx.author.id)
        gamer = get(ctx.author.guild.roles, id=798537784348114955)
        coder = get(ctx.author.guild.roles, id=780280968183152701)
        anime_weeb = get(ctx.author.guild.roles, id=798538056814297110)
        weebs = ['animeweeb','anime weeb','anime','weeb']
        balance = await self.get(ctx.author.id)
        backs = await self.available(ctx.author.id)

        for back in shopping:
            if item == back['name']:
                if balance>back['price']:
                    if item not in backs:
                        embed = discord.Embed(title = "Background for Profile Bought",description = f"{ctx.author.name} have succesfully Bought the {item.title()} Background Role ",color = random.choice(self.colors))
                        embed.set_thumbnail(url = ctx.author.avatar_url)
                        embed.set_footer(text=f"Check your Profile now by {prefix}profile")
                        await self.add(ctx.author.id,-1*back['price'])
                        await ctx.send(embed = embed)
                        backs.insert(0,item)
                        await self.update(ctx.author.id,backs)
                        return
                    else:
                        em234 = discord.Embed(description = f"{ctx.author.mention} already Have the {item.title()} background",color = discord.Colour.red())
                        await ctx.send(embed = em234,delete_after = 10)
                        return
                else:
                    await ctx.send(embed = less)
                    return
            else:
                pass
        await ctx.send(embed = discord.Embed(title = "No such Item",description=f"Please recheck the Item name and make sure that there's no Typo\nType `{prefix}shop` for the items",color=random.choice(self.colors)))




                
    @commands.command(aliases = ['hunting'])
    @commands.cooldown(1, 1000 , type = commands.BucketType.user)
    async def hunt(self,ctx):
        """Hunt down animals and sell them for credits"""
        animal = random.choice(huntanimals)
        if animal != 0:
            embed = discord.Embed(title = "Hunting Results",description = f"Nice Play , You hunted down a {animal} {animal.replace(':','')}",color = random.choice(self.colors))
            
            await self.plus(ctx.author.id,animal)
        else:
            embed = discord.Embed(title = "Hunting Results",description = "Ah You are trash at hunting, You found nothing, Better do a bit more Practice",color = random.choice(self.colors))

        embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        embed.set_footer(text = "Type .inventory to see you inventory")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

    @commands.command(aliases = ['fishing'])
    @commands.cooldown(1, 1200  , type = commands.BucketType.user)
    async def fish(self,ctx):
        """Catch fishes and sell them for credits"""
        fish = random.choice(fishcate)
        if fish != 0:
            embed = discord.Embed(title = "Fishing results",description = f"Very well done , you captured a {fish} {fish.replace(':','')}",color = random.choice(self.colors))
            await self.plus(ctx.author.id,fish)
        else:
            embed = discord.Embed(title = "Fishing results",description = f"huh, What was that!? , You found nothing :confused:",color = random.choice(self.colors))
        embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        embed.set_footer(text = "Type .inventory to see you inventory")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Economy(bot))

