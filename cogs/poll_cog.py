import datetime
from discord import app_commands, ui
from discord.ext import commands
import discord
from utils import *
from constants import *
from api import app

class polling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Create a poll")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 300)
    async def poll(self, interaction, question: str):
        pass

async def setup(bot):
    bot.add_cog(polling(bot))
    print("Polling cog loaded")