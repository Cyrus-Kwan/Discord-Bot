# PACKAGES::
import discord
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
    async def on_ready(self) -> discord.Client:
        print(f"Logged in as: {self.user}")
        return self.user

def main():
    # Bot configuration
    intents = discord.Intents.all()
    bot = Bot(intents=intents)

    # Access the database
    model = Model("bot_config.db")
    config = model.schema["bot_config"]

    # Parameters to get the access token for the specified bot
    bot_name = "cmd#7080"
    bot_token = config[config["bot_name"] == bot_name]["access_token"]

    # Run the bot using private access token
    bot.run(*bot_token)

if __name__ == "__main__":
    main()