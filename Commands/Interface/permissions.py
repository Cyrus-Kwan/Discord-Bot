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

class Permission:
    '''
    Limits interactions for command tree applications in interface.py
    '''
    def __init__(self):
        self.tokens = config.load(path="tokens.json")

    def admin(self, interaction:Interaction):
        admin:int = self.tokens["admin"]

        return interaction.user.id == admin

def main():
    return

if __name__ == "__main__":
    main()