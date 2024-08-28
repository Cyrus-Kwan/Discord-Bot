# PACKAGES::
import re
import requests
import discord
from discord import Client
from discord import app_commands
from datetime import datetime

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from commands.utils.config import General
from commands.utils.config import Emote
from commands.utils.config import Steal

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

    async def steal(self, message:str, interaction:discord.Interaction, search:str=None, rename:str=None):
        message:str = message
        emote:str = Emote.extract(message=message, search=search)
        name:str = rename if rename else Emote.name(emote=emote)
        code:str = Emote.code(emote=emote)
        guild:discord.Guild = interaction.guild
        existing_emotes:dict[int] = {emoji.name:emoji.id for emoji in guild.emojis}

        if not emote:
            return

        if name in existing_emotes:
            duplicate: str = await guild.fetch_emoji(existing_emotes[name])
            embed: discord.Embed = Steal.duplicate(emote_name=duplicate)

            await interaction.response.send_message(embed=embed)
            return
        
        if (search == None) or (search == Emote.name(emote=emote)):
            # Get the source image in byte code
            src: str = await General.url(emote=emote)
            image: str = requests.get(src).content

            # Add the new emote to the server
            new_emote:discord.Emoji = await guild.create_custom_emoji(name=name, image=image)
            return new_emote
            
        return

    # COMMANDS::
    def slash_commands(self):
        @self.tree.command(name="shutdown", description="Closes the client instance")
        async def shutdown(interaction:discord.Interaction) -> None:
            embed = await General.shutdown()

            await interaction.response.send_message(embed=embed)
            await self.client.close()

            return

        @self.tree.command(name="users", description="Returns a table containing user details")
        async def users(interaction:discord.Interaction) -> None:
            model = self.client.model
            sql: str = "SELECT * FROM users"
            user_table = await model.read(sql)

            await interaction.response.send_message(user_table)

            return

        @self.tree.command(name="steal", description="Adds the most recently messaged emote to the server")
        async def steal_history(interaction:discord.Interaction, search:str=None, rename:str=None) -> None:
            '''
            Adds the most recently sent emote in the channel to the server emotes.
            A user can target an emote by specifying the exact name.
            '''
            # Get the most recent messages
            messages:pd.Series = await General.recent_messages(
                model=self.client.model, 
                id=interaction.channel_id
                )
            
            # Loop through n previous messages until a new emote has been added
            for message in messages:
                new_emote = await self.steal(
                    message=message, interaction=interaction, search=search, rename=rename
                )
                if new_emote:
                    # Return success embed when a new emote is added
                    embed = await Steal.success(emote=str(new_emote))
                    await interaction.response.send_message(embed=embed)
                    return

            # Return missing embed if the emote was not found
            embed = await Steal.missing(emote_name=search)
            await interaction.response.send_message(embed=embed)

            return

        @self.tree.context_menu(name="steal")
        async def steal_message(interaction:discord.Interaction, message:discord.Message):
            '''
            Directly add a sole emote from a message
            '''
            new_emote = await self.steal(
                message=message.content, interaction=interaction
            )
            if new_emote:
                # Return success embed when a new emote is added
                embed = await Steal.success(emote=str(new_emote))
                await interaction.response.send_message(embed=embed)
            else:
                # Return missing embed if the emote was not found
                embed = await Steal.missing()
                await interaction.response.send_message(embed=embed)

            return


    def event_commands(self):
        @self.client.event
        async def on_message(message:discord.Message) -> None:
            if message.author.bot:
                return

            if message.content == "":
                return

            channel_id: int = message.channel.id
            message_id: int = message.id
            content: str = message.content
            reply: bool = bool(message.type == discord.MessageType.reply)
            respondent: int = message.reference.message_id if reply else None
            author: int = message.author.id

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
            return
