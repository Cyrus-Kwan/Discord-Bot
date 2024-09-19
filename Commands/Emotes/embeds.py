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
        # Stores the user'd dropdown selections and the response
        self.selection:dict = {}
        self.responses:dict = {}

        # Instantiate dropdown menus for new emote location
        emote_menu:Select = StealEmote(
            menu=emote_config,
            table=emote_table,
            selection=self.selection,
            responses=self.responses
        )
        guild_menu:Select = StealGuild(
            menu=guild_config,
            table=guild_table,
            selection=self.selection,
            responses=self.responses
        )

        # Instantiate buttons for emote select confirmation
        cancel_button = Button(
            label="Cancel", style=ButtonStyle.red
        )
        confirm_button = Button(
            label="Confirm", style=ButtonStyle.green
        )
        rename_button = Button(
            label="Rename", style=ButtonStyle.blurple
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

    async def rename(self, interaction:Interaction):
        '''Callback for rename button'''

        await interaction.response.send_message("Rename")

    async def cancel(self, interaction:Interaction):
        '''Callback for cancel button'''
        embed_config:dict = config.load(
            path="commands/emotes/steal/embeds/cancel_button.json"
        )

        # Clear selection indicator embeds
        for message in self.responses.values():
            await message.delete()

        # Clear empty map
        self.responses = {}

        # Response embed
        embed = Embed(
            title=embed_config["title"],
            colour=config.colour[embed_config["colour"]],
            description=embed_config["description"]
        )

        await interaction.response.edit_message(
            embed=embed, 
            view=embed_config["view"], 
            delete_after=embed_config["delete_after"]
        )

    async def confirm(self, interaction:Interaction):
        '''Callback for confirm button'''
        embed_config:dict = config.load(
            path="commands/emotes/steal/embeds/confirm_button.json"
        )

        # Variable handling
        emoji:Emoji = self.selection["Emote"]["emoji"]
        guild:Guild = self.selection["Server"]["guild"]

        name:str = emoji.name
        image:str = requests.get(url=emoji.url).content

        # Add selected emote to the server
        await guild.create_custom_emoji(
            name=name,
            image=image
        )
        
        # Clear selection indicator embeds
        for message in self.responses.values():
            await message.delete()

        self.responses = {}

        # Response embed
        embed = Embed(
            title=embed_config["title"],
            colour=config.colour[embed_config["colour"]],
            description=embed_config["description"].format(
                name=name, guild=guild
            )
        )
        embed.set_thumbnail(url=emoji.url)

        await interaction.response.send_message(
            embed=embed, ephemeral=True
        )
        '''
        Should also send embed to the selected guild. 
        Try and figure out which channel to send embed to
        '''

class StealEmote(Select):
    def __init__(self, menu:dict, table:dict, selection:dict, responses:dict):
        '''
        Parameters
            menu: The list of dropdown items that the menu will read as SelectOptions
            table: Option configs and objects for use in callback
            embeds: Map of existing embeds to update
        '''
        self.menu:dict = menu
        self.table:dict = table
        self.colour:dict = config.colour
        self.selection:dict = selection
        self.responses:dict = responses
        options:list = [option["label"] for option in table.values()]

        super().__init__(
            placeholder=menu["placeholder"],
            min_values=menu["min_values"],
            max_values=menu["max_values"],
            options=options
        )

    async def callback(self, interaction:Interaction):
        key:str = self.table[self.values[0]]["type"]
        self.selection[key] = self.table[self.values[0]]

        embed = Embed()
        embed.set_author(
            name=key
        )
        embed.set_footer(
            text=self.values[0], 
            icon_url=self.table[self.values[0]]["url"]
        )

        if key in self.responses.keys():
            # Modifies the Message object to the new selection
            await interaction.response.defer()
            await self.responses[key].edit(embed=embed)
        else:
            # Adds a Message object to the responses map
            await interaction.response.defer()
            self.responses[key] = await interaction.followup.send(
                embed=embed
            )

class StealGuild(Select):
    def __init__(self, menu:dict, table:dict, selection:dict, responses:dict):
        '''
        Parameters
            menu: The list of dropdown items that the menu will read as SelectOptions
            table: Option configs and objects for use in callback
            embeds: Map of existing embeds to update
        '''
        self.menu:dict = menu
        self.table:dict = table
        self.colour:dict = config.colour
        self.selection:dict = selection
        self.responses:dict = responses
        options:list = [option["label"] for option in table.values()]

        super().__init__(
            placeholder=menu["placeholder"],
            min_values=menu["min_values"],
            max_values=menu["max_values"],
            options=options
        )

    async def callback(self, interaction:Interaction):
        key:str = self.table[self.values[0]]["type"]
        self.selection[key] = self.table[self.values[0]]

        embed = Embed()
        embed.set_author(
            name=key
        )
        embed.set_footer(
            text=self.values[0], 
            icon_url=self.table[self.values[0]]["url"]
        )

        if key in self.responses.keys():
            # Modifies the Message object to the new selection
            await interaction.response.defer()
            await self.responses[key].edit(embed=embed)
        else:
            # Adds a Message object to the responses map
            await interaction.response.defer()
            self.responses[key] = await interaction.followup.send(
                embed=embed
            )