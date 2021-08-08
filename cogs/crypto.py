import discord
from discord import colour
from discord.ext import commands
import base64
import random
import datetime
from googletrans import Translator
import string

SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',  '*', '(', ')']



class Crypto(commands.Cog):
    """Commands and helps for securing data """
    def __init__(self,bot):
        self.bot = bot
        self.colors = self.bot.colors


    @commands.command(aliases = ['encodeimg'])
    async def imgenc(self, ctx):
        """Encode an Image into text (for decoding later)"""
        if len(ctx.message.attachments) <= 0:
            await ctx.send(embed = discord.Embed(description = "Make sure your msg have an image attached with it.", color = discord.Colour.red()),delete_after = 6)
            return
        url = ctx.message.attachments[0].url    
        ss = url.encode("ascii") 
        base64_bytes = base64.b64encode(ss) 
        base64_string = base64_bytes.decode("ascii") 
        base64_string = base64_string.replace("==", "")
        embed = discord.Embed(title = "Image Encoded", description = f"```{base64_string}```", color =  random.choice(self.colors))
        embed.set_footer(text="type .imgdec + encoded_code to get the decoded image")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['decodeimg'])
    async def imgdec(self, ctx,*,string):
        """Decode a Encoded string (text)"""
        string = f"{string}=="
        try:
            base64_bytes = string.encode("ascii") 
            sample_string_bytes = base64.b64decode(base64_bytes) 
            sample_string = sample_string_bytes.decode("ascii") 
            embed = discord.Embed(color = 0xFFC5A8)
            embed.set_image(url = sample_string)
            embed.set_author(name = ctx.author.name,url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(embed = discord.Embed(description = "Couldn't Decode the Code, make sure that you didn't have a typo.", color = discord.Colour.red()))

    @commands.command(aliases = ["passw","strongpass"])
    async def password(self, ctx, *, passw,length = 8):
        """Get a complex password on the basis of the key provided"""
        cap_pass = ''.join(random.choice((str.upper, str.lower))(c) for c in passw)
        var1 = ''.join('%s%s' % (x, random.choice((random.choice(SYMBOLS), ""))) for x in cap_pass)
        try:
            var1 = var1.replace(" ","")
        except:
            pass
        while len(var1)<=length:
            var1 += random.choice(SYMBOLS)

        embed = discord.Embed(description = "Generated new password for you!", color = random.choice(self.colors), timestamp = datetime.datetime.utcnow())
        embed.add_field(name = "Old Password", value = f"```{passw}```", inline = False)
        embed.add_field(name = "New Password", value = f"```{var1}```", inline = False)
        embed.add_field(name = "Length", value = f"```{len(var1)}```")
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['ranpass'])
    async def randompass(self, ctx, number: int = 6):
        """Get a random pass consisting of random characters"""
        if number > 100:
            await ctx.send(embed = discord.Embed(description = "Isn't that digit too long?", color = discord.Colour.red()))

        if number < 6:
            await ctx.send(embed = discord.Embed(description = "Isn't that digit too short?", color = discord.Colour.red()))

        def password(stringLength):
            password_character = string.ascii_letters + string.digits + string.punctuation
            return "".join(random.choice(password_character) for i in range(stringLength))

        embed = discord.Embed(color = random.choice(self.colors), timestamp = datetime.datetime.utcnow())
        embed.add_field(name = "Random Password", value = f"```{password(number)}```")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['enc'])
    async def encode(self, ctx, *, string):
        """Encode a message (text) """
        try:
            ss = string.encode("ascii") 
            base64_bytes = base64.b64encode(ss) 
            base64_string = base64_bytes.decode("ascii") 
            embed = discord.Embed(color = random.choice(self.colors))
            embed.add_field(name = "Encoded - ", value = f"```{base64_string}```")
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.set_footer(text="Type .decode + encoded_value to get the translation")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(e)
            await ctx.send(embed = discord.Embed(description = "Couldn't Encode the given string.", color = discord.Colour.red()))
    
    @commands.command(aliases = ['dec'])
    async def decode(self, ctx,*,string):
        """Decode an encoded text"""
        try:
            base64_bytes = string.encode("ascii") 
            sample_string_bytes = base64.b64decode(base64_bytes) 
            sample_string = sample_string_bytes.decode("ascii")
            embed = discord.Embed(color = random.choice(self.colors))
            embed.add_field(name = "Decoded - ", value = f"```{sample_string}```")
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed= embed)
        except:
            await ctx.send(embed = discord.Embed(description = "Couldn't Decode the Code, make sure that you didn't have a typo.",color =discord.Colour.red()))

    @commands.command(aliases = ['translate'])
    async def lang(self,ctx,*,arg):
        """Translate text of any language"""
        trans = Translator()
        trs = trans.translate(arg, dest="en")
        detected = trans.detect(arg)
        embed = discord.Embed(title = "Here is your translated text", description = f"`{trs.text}`", color = random.choice(self.colors))
        embed.set_footer(text = f"Translated from {detected.lang} to en.")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Crypto(bot))
