import discord
import sys
import numpy as np
from discord import Client
from pathlib import Path

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[4].__str__()
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
            sql:str = """
            SELECT Current, Previous FROM Graph
            """
            fetch = await self.model.read(query=sql)
            start = np.random.choice(fetch["Current"])
            stop = np.random.choice(fetch["Previous"])
            gen_str:str = await self.ngram.generate(start=start, stop=stop)
            short_str:str = await self.ngram.short(string=gen_str)
            await interaction.response.send_message(short_str)
            return

    def event_commands(self):
        @self.on_message
        async def on_mention(message:discord.Message) -> None:
            if message.author == self.client.user:
                return

            if self.client.user not in message.mentions:
                return

            sql:str = """
            SELECT Current, Previous FROM Graph
            """
            fetch = await self.model.read(query=sql)
            splits = message.content.split()
            start = np.random.choice(fetch["Current"])
            stop = np.random.choice(fetch["Previous"])

            gen_str:str = await self.ngram.generate(start=start, stop=stop)
            short_str:str = await self.ngram.short(string=gen_str)
            await message.channel.send(short_str)
            return

    def on_message(self, func):
        '''
        Decorator for commands that run on message token
        '''
        def wrapper():
            func()
        
        return wrapper