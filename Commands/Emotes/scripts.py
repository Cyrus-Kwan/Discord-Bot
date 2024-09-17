# ENVIRONMENT SETUP::
import sys
import pathlib

PARENTPATH = "Discord Bot"
PYTHONPATH = pathlib.Path(__file__)

# Iterate through the parents of the current file path
for path in PYTHONPATH.parents:
    curr_path = str(path)
    # Check if the parent directory name is in the current path
    if PARENTPATH in curr_path:
        if curr_path not in sys.path:
            sys.path.append(curr_path)
    else:
        break

from Libs.commands.emotes import *

class EmoteScript:
    def __init__(self):
        self.script_config:dict = config.load(path="commands/emotes/scripts.json")

    def content(self, message:Message):
        emote_pattern:str = self.script_config["emote_pattern"]
        name_pattern:str = self.script_config["name_pattern"]
        emote_search:list[str] = re.findall(
            pattern=emote_pattern, string=message.content
        )

        emotes:dict[Emoji] = {}
        for emote in emote_search:
            name_search:str = re.search(
                pattern=name_pattern, string=emote
            ).group()

            emotes[name_search] = PartialEmoji(
                name=name_search
            ).from_str(value=emote)

        return emotes

    def emotes(self, message:Message):
        emotes:dict = self.content(message=message)

        options:dict[SelectOption] = {}
        for name, emoji in emotes.items():
            options[name] = {
                "url":emoji.url,
                "type":"Emote",
                "label":SelectOption(label=name),
                "colour":"gold",
                "emote":emoji
            }

        return options

    def guilds(self, interaction:Interaction):
        guilds:list[Guild] = interaction.user.mutual_guilds

        options:list[SelectOption] = {}
        for guild in guilds:
            options[guild.name] = {
                "url":guild.icon,
                "type":"Server",
                "label":SelectOption(label=guild.name),
                "colour":"blurple",
                "guild":guild
            }

        return options