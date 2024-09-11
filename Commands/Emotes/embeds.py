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

class EmoteEmbed:
    def __init__(self, file:str, name:str):
        self.file = file
        self.name = name

        self.command_config:dict = config.load(path=self.file)[self.name]
        self.colour = {
            key:int(value, base=16) for key, value in config.load("colours.json").items()
        }
    
    def response(self):
        return self.embed

    def open(self):
        embed_config:dict = self.command_config["embed"]
        embed = Embed(
            title=embed_config["title"],
            description=embed_config["description"],
            colour=self.colour[embed_config["colour"]]
        )

        return embed

    def view(self, message:Message, interaction:Interaction):
        '''
        embeds: Stores embeds to be modified on dropdown selection
        emote_scrip: Used to process emotes and guilds from message and interactions
        '''
        embeds:dict = {}
        emote_script = EmoteScript(file=self.file, name=self.name)

        # View configurations for dropdown menus
        select_emote:dict = self.command_config["select"]["emotes"]
        select_guild:dict = self.command_config["select"]["guilds"]

        # Processed emote and guild elements for respective embeds
        emote_table:dict = emote_script.emotes(message=message)
        guild_table:dict = emote_script.guilds(interaction=interaction)

        # Dropdown menus
        emotes = SelectMenu(menu=select_emote, table=emote_table, embeds=embeds)
        guilds = SelectMenu(menu=select_guild, table=guild_table, embeds=embeds)

        confirm = '''Add confirm selection button'''
        cancel = '''Add cancel selection button'''

        view = SelectView(emotes, guilds)

        return view

class Confirm(Button):
    def __init__(self):
        super().__init__()

    async def callback(interaction:Interaction):
        await interaction.message.delete()
        await interaction.response.send_message("Button")

class SelectMenu(Select):
    def __init__(self, menu:dict, table:dict, embeds:dict):
        self.table:dict = table
        self.embeds:dict = embeds
        self.colour:dict = {
            key:int(value, base=16) for key, value in config.load("colours.json").items()
        }

        options:list = [value["label"] for value in table.values()]

        super().__init__(
            placeholder=menu["placeholder"],
            min_values=menu["min_values"],
            max_values=menu["max_values"],
            options=options
        )

    async def callback(self, interaction:Interaction):
        '''
        Modifies the dropdown embed response as a footer
        '''
        # User selection from dropdown menu
        select:dict = self.table[self.values[0]]
        
        # Embed response for user selection
        option = Embed(
            colour=self.colour[select["colour"]], 
        )
        option.set_footer(
            text=select["type"], icon_url=select["url"]
        )

        # Update all selected embeds to the dropdown user selections
        self.embeds["origin"] = interaction.message.embeds[0]
        self.embeds[select["type"]] = option

        await interaction.response.edit_message(embeds=self.embeds.values())

class SelectView(View):
    def __init__(self, *args, **kwargs):
        super().__init__()
        for menu in args:
            self.add_item(menu)