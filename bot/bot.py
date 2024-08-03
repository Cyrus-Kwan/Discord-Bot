# PACKAGES::
import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd
import asyncio
import sqlite3

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
    def __init__(self, intents:discord.Intents):
        super().__init__(intents=intents)

        # Class attributes for command interaction
        self.model: Model = None
            
        # App and slash command support
        self.tree: app_commands.CommandTree = app_commands.CommandTree(self)

    async def on_ready(self) -> discord.Client:
        # Create main database on startup and necessary tables
        self.model = await Model.create(database="main.db", script="users.sql")
        self.load_users()

        print(await self.model.read("SELECT * FROM users;"))

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

    async def load_users(self) -> None:
        '''Currently a very crude solution to populating the user database on startup'''
        # TODO: Populate user table with user data
        for user in self.users:
            if user.bot:
                continue

            try:
                sql = f"""
                UPDATE users SET
                user_id = {user.id},
                server_name = '{user.name}',
                global_name = '{user.global_name}'
                """
                await self.model.write(sql)
            except sqlite3.IntegrityError:
                sql = f"""
                INSERT INTO users (user_id, server_name, global_name) VALUES
                ({user.id}, '{user.name}', '{user.global_name}');
                """
                await self.model.write(sql)

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