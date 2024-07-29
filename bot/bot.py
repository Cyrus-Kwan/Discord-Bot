# PACKAGES::
import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd
import asyncio

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model
import commands

class Client(discord.Client):
    def __init__(self, intents:discord.Intents):
        super().__init__(intents=intents)

        # App and slash command support
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self) -> discord.Client:
        print(f"Logged in as: {self.user}")

        return self.user

    async def setup_hook(self) -> None:
        # Register commands here
        commands.Echo(self)
        commands.Users(self)
        commands.Shutdown(self)

        # Sync the application commands with the server
        await self.tree.sync()

async def get_token(client_name:str) -> str:
    # Access the database
    model = await Model.create("config.db")
    config = model.schema["clients"]

    # Parameters to get the access token for the specified bot
    client_token = config[config["client_name"] == client_name]["access_token"]

    return client_token[0]

if __name__ == "__main__":
    # Bot configuration
    intents = discord.Intents.all()
    client = Client(intents=intents)
    token = asyncio.run(get_token(client_name="cmd#7080"))

    # Run the bot using private access token
    client.run(token)