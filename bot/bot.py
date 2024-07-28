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

class Bot(discord.Client):
    def __init__(self, intents:discord.Intents):
        super().__init__(intents=intents)

        # App and slash command support
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self) -> discord.Client:
        print(f"Logged in as: {self.user}")

        # return self.user

    async def setup_hook(self) -> None:
        # Register commands here
        commands.Echo(self)

        # Sync the application commands with the server
        await self.tree.sync()

async def get_token(bot_name:str) -> str:
    # Access the database
    model = await Model.create("bot_config.db")
    config = model.schema["bot_config"]

    # Parameters to get the access token for the specified bot
    bot_token = config[config["bot_name"] == bot_name]["access_token"]

    return bot_token[0]

if __name__ == "__main__":
    # Bot configuration
    intents = discord.Intents.all()
    bot = Bot(intents=intents)
    token = asyncio.run(get_token(bot_name="cmd#7080"))

    # Run the bot using private access token
    bot.run(token)