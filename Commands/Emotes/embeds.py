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

class StealEmbed(Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StealView(View):
    def __init__(self, emote_config:dict, guild_config:dict, emote_table:dict, guild_table:dict):
        super().__init__()
        # Instantiate dropdown menus for new emote location
        emote_menu:Select = StealSelect(
            menu=emote_config, table=emote_table
        )
        guild_menu:Select = StealSelect(
            menu=guild_config, table=guild_table
        )

        # Instantiate buttons for emote select confirmation
        cancel_button = Button(
            label="Cancel", style=ButtonStyle.primary
        )
        confirm_button = Button(
            label="Confirm", style=ButtonStyle.primary
        )
        rename_button = Button(
            label="Rename", style=ButtonStyle.primary
        )

        # Link buttons to their callbacks
        cancel_button.callback = self.cancel
        rename_button.callback = self.rename
        confirm_button.callback = self.confirm

        # Add dropdown menus to the view
        self.add_item(emote_menu)
        self.add_item(guild_menu)

        # Add buttons after the dropdown menus
        self.add_item(cancel_button)
        self.add_item(rename_button)
        self.add_item(confirm_button)

    async def confirm(self, interaction:Interaction):
        '''Callback for confirm button'''
        await interaction.response.send_message("Confirm")

    async def rename(self, interaction:Interaction):
        '''Callback for rename button'''
        await interaction.response.send_message("Rename")

    async def cancel(self, interaction:Interaction):
        '''Callback for cancel button'''
        embed_config = config.load(
            path="commands/emotes/steal/views/cancel_button.json"
        )
        embed = Embed(
            title=embed_config
        )
        await interaction.response.send_message("Cancel")

class StealSelect(Select):
    def __init__(self, menu:dict, table:dict):
        '''
        Parameters
            menu: The list of dropdown items that the menu will read as SelectOptions
            table: Option configs and objects for use in callback
            embeds: Map of existing embeds to update
        '''
        self.menu:dict = menu
        self.table:dict = table
        self.colour = config.colour
        options:list = [option["label"] for option in table.values()]

        super().__init__(
            placeholder=menu["placeholder"],
            min_values=menu["min_values"],
            max_values=menu["max_values"],
            options=options
        )

    async def callback(self, interaction:Interaction):
        await interaction.response.send_message(content=self.values)