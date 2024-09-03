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

class Interface:
    def __init__(self, client:Client):
        self.client:Client = client
        self.tree:CommandTree = client.tree

        self.permissions = Permission()
        self.shutdown = Shutdown(file=__file__)

    @classmethod
    async def register(cls, client:Client):
        '''
        Alternate constructor for Interface object
        Used to register commands to the command tree in setup_hook
        '''
        self = cls(client)

        # Register commands
        self.menu_commands()
        self.slash_commands()
        self.event_commands()

        return self

    def menu_commands(self):
        return

    def slash_commands(self):
        @app_commands.check(
            self.permissions.admin
        )
        @app_commands.allowed_installs(
            guilds=self.shutdown.installs["guilds"],
            users=self.shutdown.installs["users"]
        )
        @app_commands.allowed_contexts(
            dms=self.shutdown.contexts["dms"],
            guilds=self.shutdown.contexts["guilds"],
            private_channels=self.shutdown.contexts["private_channels"]
        )
        @self.tree.command(
            name=self.shutdown.name,
            description=self.shutdown.description
        )
        async def shutdown(interaction:Interaction):
            '''
            Exits current runtime of bot client
            Responds with an ephemeral embed notification
            This command should only be callable by an administrator
            '''
            try:
                embed:Embed = self.shutdown.response(
                    status="pass"
                )
            except Exception:
                embed:Embed = self.shutdown.response(
                    status="fail"
                )

            await interaction.response.send_message(
                embed=embed, ephemeral=self.shutdown.ephemeral
            )
            await self.client.close()
            return

        return

    def event_commands(self):
        return

def main():
    intents = Intents().all()
    client = Client(intents=intents)
    interface = Interface(client=client)
    return

if __name__ == "__main__":
    main()