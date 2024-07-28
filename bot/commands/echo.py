import discord
from discord import app_commands 
from discord.ext import commands

class Echo():
    '''
    Messages user input in the same channel that the command was called.
    '''
    def __init__(self, bot:discord.Client):
        self.bot: discord.Client = bot
        self.tree: discord.Client.CommandTree = bot.tree

        @self.tree.command(name="echo", description="Echoes a message.")
        @app_commands.describe(message="Message to echo.")
        async def echo(interaction:discord.Interaction, message:str) -> None:
            await interaction.response.send_message(message)