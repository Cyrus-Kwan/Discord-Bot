import discord
import sys
from discord import Client
from pathlib import Path

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

from commands.chat.ngram.ngram import NGram
from commands.chat.ngram.graph import Graph
from models.model import Model

class Chat():
    '''
    Functionality to send model-generated messages in response to a user interaction or certain prompts.
    '''
    # CONSTRUCTOR::
    def __init__(self, client:Client):
        self.client:Client = client
        self.model:Model = self.client.model
        self.tree:discord.Client.CommandTree = client.tree
        self.ngram:Ngram = NGram(model=self.model)
        self.graph:Graph = None

    @classmethod
    async def register(cls, client:Client):
        self = cls(client=client)

        # Setup table for message logging
        await self.client.model.inject("messages.sql")
        self.graph:Graph = await Graph.create(database="main.db", script="ngram.sql")

        # Register commands
        self.slash_commands()
        self.event_commands()

        return self

    # COMMANDS::
    def slash_commands(self):
        @self.tree.command(name="chat", description="Sends a generated message into the same channel the method was called.")
        async def chat(interaction:discord.Interaction) -> None:
            gen_str:str = await self.ngram.generate()   # Define some start and stop string
            short_str:str = await self.ngram.short(string=gen_str)
            await interaction.response.send_message(short)
            return

    def event_commands(self):
        @self.client.event
        async def on_mention(message:discord.Message) -> None:
            gen_str:str = await self.ngram.generate()   # Define some start and stop string
            short_str:str = await self.ngram.short(string=gen_str)
            await interaction.response.send_message(short)
            return