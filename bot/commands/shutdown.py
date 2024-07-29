import discord
from discord import app_commands 
from discord.ext import commands

class Shutdown():
    '''
    Shuts down the bot.
    '''
    def __init__(self, client:discord.Client):
        self.client: discord.Client = client
        self.tree: discord.Client.CommandTree = client.tree

        @self.tree.command(name="shutdown", description="Closes the client instance")
        async def shutdown(interaction:discord.Interaction) -> None:
            await interaction.response.send_message("Feeling sleepy...")
            await client.close()