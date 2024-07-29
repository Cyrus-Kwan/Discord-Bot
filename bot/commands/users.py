import discord
from discord import app_commands 
from discord.ext import commands

class Users():
    '''
    Messages all user details in the same channel that the command was called.
    '''
    def __init__(self, client:discord.Client):
        self.client: discord.Client = client
        self.tree: discord.Client.CommandTree = client.tree

        @self.tree.command(name="users", description="all users in the server")
        async def users(interaction:discord.Interaction) -> None:
            users = self.client.users
            await interaction.response.send_message(users)