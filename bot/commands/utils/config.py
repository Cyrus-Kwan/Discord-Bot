# PACKAGES::
import discord
import re
import pandas as pd
import asyncio

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[3].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model

class General():
    @staticmethod
    async def shutdown():
        embed = discord.Embed(
            color=discord.Color.brand_green(),
            description="Feeling sleepy...",
            title="Shutdown"
        )

        return embed

    @staticmethod
    async def url(emote:str):
        pattern: str = r"^<a:"
        animated = re.search(pattern=pattern, string=emote)
        code = Emote.code(emote=emote)
        if animated:
            return f"https://cdn.discordapp.com/emojis/{code}.gif?size=96&quality=lossless"
        else:
            return f"https://cdn.discordapp.com/emojis/{code}.webp?size=96&quality=lossless"

    @staticmethod
    async def recent_messages(model:Model, id:int, n:int=50):
        sql = f"""
        SELECT content 
        FROM messages 
        WHERE channel_id = {id}
        ORDER BY date_created DESC
        LIMIT {n};
        """
        messages: pd.DataFrame = await model.read(sql)

        return messages["content"]

    @staticmethod
    async def table(data:pd.DataFrame):
        '''
        Returns formatted embed for a pandas dataframe
        '''
        return

class Steal():
    color_map = {
    "brand red": discord.Color.brand_red(),
    "brand green": discord.Color.brand_green()
    }

    @staticmethod
    def duplicate(emote_name:str):
        embed = discord.Embed(
            color=discord.Color.brand_red(),
            description=f"The emote {emote_name} already exists.",
            title="ERROR | Duplicate Emote"
        )

        return embed

    @staticmethod
    async def missing(emote_name:str=None):
        embed = None
        if emote_name:
            embed = discord.Embed(
                color=discord.Color.brand_red(),
                description=f"No emote **`{emote_name}`** found.",
                title="ERROR | Emote not found"
            )
        else:
            embed = discord.Embed(
                color=discord.Color.brand_red(),
                description=f"No emote found.",
                title="ERROR | Emote not found"
            )

        return embed

    @staticmethod
    async def success(emote:discord.Emoji):
        name = Emote.name(emote)
        embed = discord.Embed(
            title="Steal",
            description=f"SUCCESS | A new emote **`{name}`** was successfully added to the server!",
            color=discord.Color.brand_green()
        )

        url = await General.url(emote=emote)
        embed.set_thumbnail(url=url)

        return embed

class Emote():
    @staticmethod
    def name(emote:str) -> str:
        if not emote:
            return

        pattern: str = r"(?:[a-zA-Z0-9_~]+)[a-zA-Z0-9_~]+(?=:)"
        result = re.search(pattern=pattern, string=emote)

        return result.group() if result else None

    @staticmethod
    def code(emote:str) -> str:
        if not emote:
            return

        pattern: str = r"(?:)(?=[0-9]+>)[0-9]+"
        result = re.search(pattern=pattern, string=emote)

        return result.group() if result else None

    @staticmethod
    def extract(message:str, search:str=None) -> str:
        result: str = None

        emote_pattern: str = r"<a?:[a-zA-Z0-9_~]+:[0-9]+>"
        search_pattern: str = f"<a?:{search}:[0-9]+>"

        if search:
            result: str = re.search(pattern=search_pattern, string=message)
        else:
            result:str  = re.search(pattern=emote_pattern, string=message)

        return result.group() if result else None

async def main():
    mod = await Model.create("main.db")
    content = await General.recent_messages(mod, 1272532155641233439)

    for message in content:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())