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

'''
Embed constructors for application commands in interface.py
'''
colour:dict = {
    key:int(value, base=16) for key, value in config.load("colours.json").items()
}

class InterfaceEmbed:
    def __init__(self, file:str, name:str):
        self.command_config:dict = config.load(path=file)[name]

    def response(self, status:str):
        embed_config:dict = self.command_config["embed"][status]

        embed = Embed(
            title=embed_config["title"],
            description=embed_config["description"],
            colour=colour[embed_config["colour"]]
        )

        return embed

def main():
    return

if __name__ == "__main__":
    main()