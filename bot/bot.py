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

from Libs.bot import *

class Client(discord.Client):
    def __init__(self, intents:discord.Intents):
        super().__init__(intents=intents)

        # Data storage for bot tokens and server resources
        self.model:Model = None

        # Represents a container that holds application command information
        self.tree:CommandTree = CommandTree(self)

        # Decorators for application commands to call when the given event occurs
        self.trigger:Trigger = Trigger(client=self)

    async def setup_hook(self):
        await Interface.register(client=self)
        await Emotes.register(client=self)

        await self.tree.sync()
        return
    
def main():
    token = config.load("tokens.json")["bot"]
    intents = discord.Intents.all()
    client = Client(intents=intents)
    client.run(token=token)
    return

if __name__ == "__main__":
    main()