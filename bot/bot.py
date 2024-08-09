# PACKAGES::
import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd
import asyncio
import sqlite3
import re

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model
import models.scripts as scripts
import commands

class Client(discord.Client):
    # CONSTRUCTOR::
    def __init__(self, intents:discord.Intents):
        super().__init__(intents=intents)

        # Class attributes for command interaction
        self.model: Model = None
            
        # App and slash command support
        self.tree: app_commands.CommandTree = app_commands.CommandTree(self)

    async def on_ready(self) -> discord.Client:
        # Create main database on startup and necessary tables
        self.model = await Model.create(database="main.db", script="users.sql")
        await self.load_users()

        print(f"Logged in as: {self.user}")

        return self.user

    async def setup_hook(self) -> None:
        '''
        Coroutine called to setup the bot.
        Asynchronously registers the specified commands from ".commands/"
        '''
        # Register commands here
        commands.Echo(self)
        commands.Users(self)
        commands.Shutdown(self)

        # Sync the application commands with the server
        await self.tree.sync()

    # USER UTILITIES::
    async def load_users(self) -> None:
        '''
        Calls an upsert on the users table
        '''
        # TODO: Populate user table with user data
        for user in self.users:
            if user.bot:
                continue
            
            target = await self.user_map(user)
            await self.model.update(table="users", values=target)

    async def user_map(self, user:discord.User) -> dict:
        '''
        Method returns a dictionary of all non-callable attributes in a User object.
        '''
        user_map: dict = {}
        pattern: str = r"^[^_].*[^_]$"
        public = lambda attr: re.search(pattern=pattern, string=attr)
        method = lambda attr: callable(getattr(user, attr))
        for attribute in user.__dir__():
            if public(attribute) and not method(attribute):
                user_map[attribute] = getattr(user, attribute)

        return user_map

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