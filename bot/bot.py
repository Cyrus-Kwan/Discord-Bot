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

    async def on_message(self, message:discord.Message):
        if message.author == self.user:
            return

        await message.channel.send()

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
    bot = Bot(intents=intents)

    # Run the bot using private access token
    bot.run(get_token("cmd#7080"))

if __name__ == "__main__":
    main()