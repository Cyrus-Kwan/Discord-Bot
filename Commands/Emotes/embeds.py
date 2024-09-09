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

class EmoteEmbed:
    def __init__(self, file:str, name:str, *args, **kwargs):
        self.command_config:dict = config.load(path=file)[name]
        self.embed:Embed = getattr(self, name=name)(*args, **kwargs)
        self.colour = {
            key:int(value, base=16) for key, value in config.load("colours.json").items()
        }
    
    def response(self):
        return self.embed

    def steal(self, status:str, emotes:dict, mutual_guilds:list):
        embed_config = self.command_config["steal"]["embed"][status]

        embed = Embed(
            title=embed_config["title"],
            colour=self.colour[embed_config["colour"]]
        )

        return