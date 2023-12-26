import datetime
from discord import app_commands, ui
from discord.ext import commands
import discord
from utils import *
from constants import *
from api import app


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def unban_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        banned_users = await interaction.guild.bans()
        print(banned_users)
        return [app_commands.Choice(name=f"{ban_entry.user.name}", value=str(ban_entry.user.id)) for ban_entry in banned_users]

    @app_commands.command(name="ban", description="Bans a user from the server")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(user = "The user to ban", reason="The reason for banning the user")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, *, reason:str|None = None):

        await interaction.guild.ban(user, reason=reason)

        embed = discord.Embed(
            title="User Banned",
            description=f"{user.mention} was banned from the server",
            color=discord.Color.brand_red(),
        )

        embed.add_field(name=f"User Id `{user.id}`", value="** **", inline=False)
        embed.add_field(name=f"Banned By {interaction.user.mention}", value="** **", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)

        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed.set_thumbnail(url=user.default_avatar.url)

        embed.set_footer(text=f"{user.name} Banned at `{datetime.datetime.utcnow()}`")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unban", description="Unbans a user from the server")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.autocomplete(user=unban_autocomplete)
    async def unban(self, interaction, user: str):
        user = await self.bot.fetch_user(user)
        await interaction.guild.unban(user)

        embed = discord.Embed(
            title="User Unbanned",
            description=f"{user.mention} was unbanned from the server",
            color=discord.Color.green(),
        )

        embed.add_field(name=f"User Id   `{user.id}`", value="** **", inline=False)
        embed.add_field(name=f"Unbanned By {interaction.user.mention}", value="** **", inline=False)

        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed.set_thumbnail(url=user.default_avatar.url)

        embed.set_footer(text=f"{user.name} Unbanned at `{datetime.datetime.utcnow()}`")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="kick", description="Kicks a user from the server")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(user = "The user to kick", reason="The reason for kicking the user")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, *, reason:str|None = None):
        await interaction.guild.kick(user, reason=reason)

        embed = discord.Embed(
            title="User Kicked",
            description=f"{user.mention} was kicked from the server",
            color=discord.Color.orange(),
        )

        embed.add_field(name=f"User Id `{user.id}`", value="** **", inline=False)
        embed.add_field(name=f"Kicked By {interaction.user.mention}", value="** **", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)

        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed.set_thumbnail(url=user.default_avatar.url)

        embed.set_footer(text=f"{user.name} Kicked at {datetime.datetime.utcnow()}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purge", description="Purges a certain amount of messages")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(amount = "The amount of messages to purge")
    async def purge(self, ctx, amount: int):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"Purged {amount} messages")
        else:
            await ctx.send("You don't have the permissions to do that!")

    @app_commands.command(name="slowmode", description="Sets a slowmode for a channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(time= "The time in seconds for the slowmode", channel="The channel to set the slowmode in")
    async def slowmode(self, interaction, time: int, channel: discord.TextChannel = None):
        if time > 21600:
            await interaction.response.send_message(embed=discord.Embed(description="Slow Mode cannot be more than 6 hours.", color=discord.Color.red()), ephemeral=True)
            return

        if time < 0:
            await interaction.response.send_message(embed=discord.Embed(description="Slow Mode cannot be less than 0 seconds.", color=discord.Color.red()), ephemeral=True)
            return

        await interaction.response.defer()

        if channel is None:
            channel = interaction.channel
        await channel.edit(slowmode_delay=time)
        embed = discord.Embed(
            title="Slowmode Set",
            description=f"Set the slowmode to `{time} seconds`",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Slowmode set at {datetime.datetime.utcnow()}")
        embed.add_field(name="Channel", value=channel.mention, inline=False)

        await interaction.followup.send(embed=embed)

    # @app_commands.guild_only()
    # @app_commands.default_permissions(administrator=True)
    # async def nuke(self, ctx):
    #     if ctx.author.guild_permissions.manage_channels:
    #         channel = ctx.channel
    #         new_channel = await channel.clone()
    #         await channel.delete()
    #         await new_channel.send("This channel has been nuked!")
    #     else:
    #         await ctx.send("You don't have the permissions to do that!")

    @app_commands.command(name="add-role", description="Adds a role to a user")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(user="The user to add the role to", role="The role to add to the user")
    async def add_role(self, interaction, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        embed = discord.Embed(
            title="Role Added",
            description=f"Added the role {role.mention} to {user.mention}",
            color=discord.Color.green(),
        )
        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed.set_thumbnail(url=user.default_avatar.url)
        embed.set_footer(text=f"Role added at {datetime.datetime.utcnow()}")
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="remove-role", description="Removes a role from a user")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(user="The user to remove the role from", role="The role to remove from the user")
    async def removerole(self, interaction, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            embed = discord.Embed(
                title="Role Removed",
                description=f"Removed the role {role.mention} from {user.mention}",
                color=discord.Color.red(),
            )
            try:
                embed.set_thumbnail(url=user.avatar.url)
            except:
                embed.set_thumbnail(url=user.default_avatar.url)
            embed.set_footer(text=f"Role removed at {datetime.datetime.utcnow()}")

            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Role Not Found",
                description=f"{user.mention} doesn't have the role {role.mention}",
                color=discord.Color.red(),
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="create-channel", description="Creates a channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(name="The name of the channel", category="The category to create the channel in", private="Whether the channel should be private or not")
    async def createchannel(self, interaction, name: str, category: discord.CategoryChannel = None, private: bool = False):
        if not private:
            await interaction.guild.create_text_channel(name=name, category=category)
        else:
            await interaction.guild.create_text_channel(name=name, category=category, overwrites={interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)})

        embed = discord.Embed(
            title="Channel Created",
            description=f"Created the channel `{name}`",
            color=discord.Color.green(),
        )
        embed.set_footer(text=f"Channel created at {datetime.datetime.utcnow()}")

        if category:
            embed.add_field(name="Category", value=category.mention, inline=False)

        await interaction.response.send_message(embed=embed) if not private else await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="delete-channel", description="Deletes a channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel="The channel to delete")
    async def deletechannel(self, interaction, channel: discord.TextChannel):
        await channel.delete()
        embed = discord.Embed(
            title="Channel Deleted",
            description=f"Deleted the channel `{channel.name}`",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Channel deleted at {datetime.datetime.utcnow()}")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(moderation(bot))
    print("Loaded moderation_cog.py")