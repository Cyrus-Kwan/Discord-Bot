# PACKAGES::
import discord
from discord import app_commands
import pandas as pd

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model

class Bot(discord.Client):
    def __init__(self, bot_name:str, intents:discord.Intents):
        super().__init__(intents=intents)

        # App and slash command support
        self.tree = app_commands.CommandTree(self)

        # Run the bot using private access token
        self.run(get_token(bot_name=bot_name))

    async def on_ready(self) -> discord.Client:
        print(f"Logged in as: {self.user}")
        return self.user

    # TODO: Figure out why this works
    async def setup_hook(self) -> None:
        # Register commands here
        @self.tree.command(name="echo", description="Echoes a message.")
        @app_commands.describe(message="The message to echo.")
        async def echo(interaction:discord.Interaction, message:str) -> None:
            await interaction.response.send_message(message)

        # Sync the application commands with the server
        await self.tree.sync()

def get_token(bot_name:str) -> str:
    # Access the database
    model = Model("bot_config.db")
    config = model.schema["bot_config"]

    # Parameters to get the access token for the specified bot
    bot_token = config[config["bot_name"] == bot_name]["access_token"]

    return bot_token[0]

def main():
    # Bot configuration
    intents = discord.Intents.all()
    bot = Bot(bot_name="cmd#7080", intents=intents)

if __name__ == "__main__":
    main()