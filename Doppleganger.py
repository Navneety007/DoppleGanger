import discord
from discord.ext import commands
import asyncpg
import os

class Doppleganger(commands.Bot):
    def __init__(self,**options):
        super().__init__(
            command_prefix = ".", 
            help_command=None, 
            description="Bot with amazing Economy, Profile, Guild, welcome etc. commands",
            case_insensitive = True,
            intents = discord.Intents.all(),
            owner_id = 779743087572025354,
            allowed_mentions = discord.AllowedMentions(everyone = False, roles = False),
             **options)

        self.colors = [0x0dd2ff,0x03f5ff,0x2affa9,0x18e6ff,0x17ffc2,0x03f5ff,0x30e79d]
    
        self.loop.run_until_complete(self.create_db_pool())

    
    async def create_db_pool(self):
        self.pg_con = await asyncpg.create_pool(os.environ['DATABASE_URL'],ssl = "require")
        
