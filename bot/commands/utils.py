# PACKAGES::
import re
import requests
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
            embed = discord.Embed(
                color=discord.Color.brand_green(),
                description="Feeling sleepy...",
                title="Shutdown"
            )

            await interaction.response.send_message(embed=embed)
            await self.client.close()

        @self.tree.command(name="users", description="Returns a table containing user details")
        async def users(interaction:discord.Interaction) -> None:
            model = self.client.model
            sql: str = "SELECT * FROM users"
            user_table = await model.read(sql)

            await interaction.response.send_message(user_table)

        @self.tree.command(name="steal", description="Adds the most recently messaged emote to the server")
        async def steal(interaction:discord.Interaction, target:str=None):
            '''
            Adds the most recently sent emote in the channel to the server emotes.
            A user can target an emote by specifying the exact name.
            '''
            # TODO: Raise exception if the emote was not found
            # TODO: Do not add duplicate emotes
            # TODO: Embed new emote notification
            emote_pattern: str = r"<a?:[a-zA-Z0-9_~]+:[0-9]+>"
            target_pattern:str = f"<a?:{target}:[0-9]+>"
            name_pattern: str = r"(?:[a-zA-Z0-9_~]+)[a-zA-Z0-9_~]+(?=:)"
            id_pattern:str = r"(?:)(?=[0-9]+>)[0-9]+"

            # Abstraction for easier readability
            row: pd.DataFrame = self.client.model.schema["messages"]
            messages: pd.Series = row[row["channel_id"]==interaction.channel_id]["content"]

            existing_emotes: dict[int] = {emoji.name:emoji.id for emoji in interaction.guild.emojis}
            
            for message in messages.sort_values(ascending=False):
                try:
                    if target:
                        emote: str = re.search(pattern=target_pattern, string=message).group()
                    else:
                        emote: str = re.search(pattern=emote_pattern, string=message).group()
                except AttributeError:
                    embed = discord.Embed(
                        color=discord.Color.brand_red(),
                        title="ERROR >> No emote found..."
                    )
                    await interaction.response.send_message(embed=embed)
                    return

                emote_name: str = re.search(pattern=name_pattern, string=emote).group()
                emote_id: str = re.search(pattern=id_pattern, string=emote).group()

                if emote_name in existing_emotes:
                    duplicate = await interaction.guild.fetch_emoji(existing_emotes[emote_name])
                    embed = discord.Embed(
                        color=discord.Color.brand_red(),
                        description=f"The emote {duplicate} already exists.",
                        title="ERROR >> Duplicate Emote"
                    )
                    await interaction.response.send_message(embed=embed)
                    return
                else:
                    src_url: str = f"https://cdn.discordapp.com/emojis/{emote_id}.webp?size=96&quality=lossless"
                    request = requests.get(src_url)

                    # Add the new emote to the server
                    new_emote = await interaction.guild.create_custom_emoji(name=emote_name, image=request.content)
                    new_url: str = f"https://cdn.discordapp.com/emojis/{new_emote.id}.webp?size=96&quality=lossless"
                    embed = discord.Embed(
                        color=discord.Color.brand_green(),
                        title="New emote",
                        description=f"The emote `{emote_name}` was added to the server!"
                    )
                    embed.set_image(url=new_url)

                    await interaction.response.send_message(embed=embed)
                    return

            return

    def event_commands(self):
        @self.client.event
        async def on_message(message:discord.Message):
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