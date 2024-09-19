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
        # Client command linking
        self.client:Client = client
        self.tree:CommandTree = client.tree
        self.trigger:Trigger = client.trigger

        # Command configs
        self.permissions = Permission()
        self.start = config.load(
            path="commands/interface/start/config.json"
        )
        self.shutdown = config.load(
            path="commands/interface/shutdown/config.json"
        )

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
        self.trigger.register()

        return self

    def menu_commands(self):
        return

    def slash_commands(self):
        @app_commands.check(
            self.permissions.admin
        )
        @app_commands.allowed_installs(
            guilds=self.shutdown["installs"]["guilds"],
            users=self.shutdown["installs"]["users"]
        )
        @app_commands.allowed_contexts(
            dms=self.shutdown["contexts"]["dms"],
            guilds=self.shutdown["contexts"]["guilds"],
            private_channels=self.shutdown["contexts"]["private_channels"]
        )
        @self.tree.command(
            name=self.shutdown["name"],
            description=self.shutdown["description"]
        )
        async def shutdown(interaction:Interaction):
            '''
            Exits current runtime of bot client
            Responds with an ephemeral embed notification
            This command should only be callable by an administrator
            '''
            try:
                embed:Embed = ShutdownEmbed(status="pass")
            except Exception:
                embed:Embed = ShutdownEmbed(status="fail")

            await interaction.user.send(embed=embed)
            await interaction.response.send_message(
                embed=embed, 
                ephemeral=self.shutdown["ephemeral"]
            )

            await self.client.close()
            return

        return

    def event_commands(self):
        @self.trigger.listen(
            event_name="on_ready"
        )
        @app_commands.allowed_installs(
            guilds=self.start["installs"]["guilds"],
            users=self.start["installs"]["users"]
        )
        @app_commands.allowed_contexts(
            dms=self.start["contexts"]["dms"],
            guilds=self.start["contexts"]["guilds"],
            private_channels=self.start["contexts"]["private_channels"]
        )
        async def start():
            '''
            Notification on new bot client runtime
            Sends notification to administrator
            '''
            try:
                embed:Embed = StartEmbed(status="pass")
            except Exception:
                embed:Embed = StartEmbed(status="fail")

            # Sends start message to administrator
            admin:User = await self.client.fetch_user(
                self.permissions.tokens["admin"]
            )
            await admin.send(
                embed=embed,
                ephemeral=self.start["ephemeral"]
            )

            return

        return

def main():
    intents = Intents().all()
    client = Client(intents=intents)
    interface = Interface(client=client)
    return

if __name__ == "__main__":
    main()