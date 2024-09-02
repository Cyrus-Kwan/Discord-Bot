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

colour:dict = config.load("colours.json")

class Shutdown:
    def __init__(self, file:str):
        config = config.load(file)["shutdown"]
        self.name = config["name"]
        self.close = config["close"]
        self.error = config["error"]
        self.installs = config["installs"]
        self.description = config["description"]

    def pass_embed(self):
        return

    def fail_embed(self):
        return
