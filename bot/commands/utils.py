# PACKAGES::
import discord
from discord import app_commands
from datetime import datetime

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from bot import *

class Utils():
    '''
    General bot commands for quality of life utility
    '''
    # CONSTRUCTOR::
    def __init__(self, client:Client):
        self.client: Client = client
        self.tree: discord.Client.CommandTree = client.tree

    @classmethod
    async def register(cls, client:Client):
        self = cls(client=client)

        # Setup table for message logging
        await self.client.model.inject("messages.sql")

        # Register commands
        self.slash_commands()
        self.event_commands()

        return self

    # COMMANDS::
    def slash_commands(self):
        @self.tree.command(name="shutdown", description="Closes the client instance")
        async def shutdown(interaction:discord.Interaction) -> None:
            await interaction.response.send_message("Feeling sleepy...")
            await self.client.close()

        @self.tree.command(name="users", description="Returns a table containing user details")
        async def users(interaction:discord.Interaction) -> None:
            model = self.client.model
            sql: str = "SELECT * FROM users"
            user_table = await model.read(sql)

            await interaction.response.send_message(user_table)

        @self.tree.command(name="steal", description="Adds the most recently messaged emote to the server")
        async def steal(interaction:discord.Interaction):
            # TODO: store user messages
            await interaction.response.send_message("WIP")

    def event_commands(self):
        @self.client.event
        async def on_message(message:discord.Message):
            if message.author.bot:
                return

            channel_id = message.channel.id
            message_id = message.id
            content = message.content
            reply = bool(message.type == discord.MessageType.reply)
            respondent = message.reference.message_id if reply else None
            author = message.author.id

            insert = {
                "message_id":message_id, 
                "channel_id":channel_id, 
                "content":content, 
                "reply":reply, 
                "respondent":respondent, 
                "author":author,
                "date_created": datetime.now(), 
            }

            await self.client.model.upsert("messages", insert)