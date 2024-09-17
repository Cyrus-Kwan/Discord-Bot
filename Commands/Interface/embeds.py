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

from Libs.commands.interface import *

class StartEmbed(Embed):
    def __init__(self, status:str):
        embed_config:dict = config.load(
            path="commands/interface/start/embeds/main.json"
        )[status]

        super().__init__(
            title=embed_config["title"],
            description=embed_config["description"],
            colour=config.colour[embed_config["colour"]]
        )

class ShutdownEmbed(Embed):
    def __init__(self, status:str):
        embed_config:dict = config.load(
            path="commands/interface/shutdown/embeds/main.json"
        )[status]

        super().__init__(
            title=embed_config["title"],
            description=embed_config["description"],
            colour=config.colour[embed_config["colour"]]
        )

def main():
    return

if __name__ == "__main__":
    main()