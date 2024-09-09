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

class Emotes:
    def __init__(self, client:Client):
        self.client:Client = client
        self.tree:CommandTree = client.tree
        self.trigger:Trigger = client.trigger

        # Command constants
        self.permissions = Permission()
        self.steal = EmotesEmbed(
            file=__file__, name="steal"
        ).command_config

    @classmethod
    async def register(cls, client:Client):
        '''
        Alternate constructor for Emotes object
        Used to register commands to the command tree in setup_hook
        '''
        self = cls(client)

        # Register commands
        self.menu_commands()
        self.slash_commands()
        self.event_commands()

        return self

    def menu_commands(self):
        @app_commands.allowed_installs(
            guilds=self.steal["installs"]["guilds"],
            users=self.steal["installs"]["users"]
        )
        @app_commands.allowed_contexts(
            dms=self.steal["contexts"]["dms"],
            guilds=self.steal["contexts"]["guilds"],
            private_channels=self.steal["contexts"]["private_channels"]
        )
        @self.tree.context_menu(
            name=self.steal["name"]
        )
        async def steal(interaction:Interaction, message:Message):
            '''
            Responds with an ephemeral embed where the user can interact
            Users should only be allowed to add emotes to servers that they
            share with the client
            Fields:
                servers - list of user and bot shared servers
                emote - list of the available emotes in the selected message
                rename - what to rename the emote
            '''
            script:EmoteScript = EmoteScript(
                file=__file__, name=self.steal["name"]
            )
            emotes:dict[str] = script.content(message=message)
            mutuals:list[Guild] = interaction.user.mutual_guilds()

            return
        return

    def slash_commands(self):
        return

    def event_commands(self):
        return