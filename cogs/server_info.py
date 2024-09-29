import datetime
from discord import app_commands, ui
from discord.ext import commands
import discord
from utils import *
from constants import *
from api import app
import aiohttp

class server_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="member-count", description="Get the number of members in the server")
    @app_commands.guild_only()
    async def member_count(self, interaction:discord.Interaction):
        human_members = len([member for member in interaction.guild.members if not member.bot])

        embed = discord.Embed(
            title="Member Count",
            description=f"Total Members: {len(interaction.guild.members)}",
            color=discord.Color.green()
        )

        embed.add_field(name="Humans", value=f"```{human_members}```", inline=True)
        embed.add_field(name="Bots", value=f"```{len(interaction.guild.members) - human_members}```", inline=True)

        embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(server_info(bot))
    print("Loaded server_info.py")