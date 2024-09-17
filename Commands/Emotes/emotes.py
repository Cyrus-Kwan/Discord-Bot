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
        self.config:dict = config.load(path=__file__)

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
            guilds=self.config["steal"]["installs"]["guilds"],
            users=self.config["steal"]["installs"]["users"]
        )
        @app_commands.allowed_contexts(
            dms=self.config["steal"]["contexts"]["dms"],
            guilds=self.config["steal"]["contexts"]["guilds"],
            private_channels=self.config["steal"]["contexts"]["private_channels"]
        )
        @self.tree.context_menu(
            name=self.config["steal"]["name"]
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
            # Emote and view field constants acquired from emotes.json
            embed_config:dict = self.config["steal"]["embed"]
            view_config:dict = self.config["steal"]["select"]
            emote_config:dict = view_config["emotes"]
            guild_config:dict = view_config["guilds"]

            # Emote and view fields based on the selected message/interaction
            emote_table:dict = EmoteScript(
                file=__file__, name="steal"
            ).emotes(message=message)
            guild_table:dict = EmoteScript(
                file=__file__, name="steal"
            ).guilds(interaction=interaction)

            # Primary display embed that notifies the user of command in use
            embed = StealEmbed(
                title=embed_config["title"],
                colour=config.colour[embed_config["colour"]],
                description="\n".join(embed_config["description"])
            )

            # Interactive elements for user to select desired emote
            view = StealView(
                emote_config=emote_config,
                guild_config=guild_config,
                emote_table=emote_table,
                guild_table=guild_table
            )

            await interaction.response.send_message(embed=embed, view=view)

            return
        return

    def slash_commands(self):
        return

    def event_commands(self):
        return