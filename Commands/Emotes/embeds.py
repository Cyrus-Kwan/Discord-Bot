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
        # Stores the users dropdown selections and the response
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
        cancel_button = CancelButton(
            selection=self.selection, responses=self.responses
        )
        rename_button = RenameButton(
            selection=self.selection, responses=self.responses
        )
        confirm_button = ConfirmButton(
            selection=self.selection, responses=self.responses
        )

        # Add dropdown menus to the view
        self.add_item(emote_menu)
        self.add_item(guild_menu)

        # Add buttons after the dropdown menus
        self.add_item(cancel_button)
        self.add_item(rename_button)
        self.add_item(confirm_button)

class CancelButton(Button):
    def __init__(self, selection:dict, responses:dict):
        self.selection:dict = selection
        self.responses:dict = responses

        super().__init__(
            label="Cancel", style=ButtonStyle.red
        )

    async def callback(self, interaction:Interaction):
        '''Callback for cancel button'''
        embed_config:dict = config.load(
            path="commands/emotes/steal/embeds/cancel_button.json"
        )
        colour:dict = config.colour

        # Response embed
        embed = Embed(
            title=embed_config["title"],
            colour=config.colour[embed_config["colour"]],
            description=embed_config["description"]
        )

        # Clear selection indicator embeds
        for message in self.responses.values():
            print(self.responses)
            await message.delete()

        # Clear empty map
        self.responses = {}

        await interaction.response.edit_message(
            embed=embed, 
            view=embed_config["view"], 
            delete_after=embed_config["delete_after"]
        )

class RenameButton(Button):
    def __init__(self, selection:dict, responses:dict):
        self.selection:dict = selection
        self.responses:dict = responses

        super().__init__(
            label="Rename", style=ButtonStyle.blurple
        )
    
    async def callback(self, interaction:Interaction):
        '''Callback for rename button'''
        modal = StealModal(
            selection=self.selection,
            responses=self.responses
        )
        await interaction.response.send_modal(modal)

class ConfirmButton(Button):
    def __init__(self, selection:dict, responses:dict):
        self.selection:dict = selection
        self.responses:dict = responses

        super().__init__(
            label="Confirm", style=ButtonStyle.green
        )

    async def valid_selection(self):
        '''
        Conditions:
            1. Emote has been selected
            2. Server has been selected
            3. Emote is unique in the selected server
            4. Server has vacant emote slots
        '''
        emote:Emoji = self.selection["Emote"]["emoji"]
        guild:GUild = self.selection["Server"]["guild"]
        guild_emote = await guild.fetch_emojis()
        emote_names = [emoji.name for emoji in guild_emote]
        emote_limit = guild.emoji_limit

        if "Emote" not in self.selection.keys():
            return False
        
        if "Server" not in self.selection.keys():
            return False

        if emote.name in emote_names:
            return False

        if len(emote_names) >= emote_limit:
            return False

        return True

    async def callback(self, interaction:Interaction):
        '''Callback for confirm button'''
        embed_config:dict = config.load(
            path="commands/emotes/steal/embeds/confirm_button.json"
        )
        error_config:dict = config.load(
            path="commands/emotes/steal/embeds/confirm_error.json"
        )

        # Check if the selections meet the requirements for adding
        valid:bool = await self.valid_selection()

        # Error embed
        error = Embed(
            title=error_config["title"],
            colour=config.colour[error_config["colour"]],
            description=error_config["description"]
        )

        # Check if valid emote selections have been made
        if not valid:
            await interaction.response.send_message(
                embed=error, ephemeral=error_config["ephemeral"]
            )
            return

        # Variable handling
        emoji:Emoji = self.selection["Emote"]["emoji"]
        guild:Guild = self.selection["Server"]["guild"]
        
        name:str = emoji.name
        image:str = requests.get(url=emoji.url).content

        # Response embed
        embed = Embed(
            title=embed_config["title"],
            colour=config.colour[embed_config["colour"]],
            description=embed_config["description"].format(
                name=name, guild=guild
            )
        )
        embed.set_thumbnail(url=emoji.url)

        # Add selected emote to the server
        await guild.create_custom_emoji(
            name=name,
            image=image
        )

        # Clear selection indicator embeds
        for message in self.responses.values():
            await message.delete()

        self.responses = {}

        await interaction.response.send_message(
            embed=embed, ephemeral=embed_config["ephemeral"]
        )

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
        self.selection:dict = selection
        self.responses:dict = responses
        options:list = [option["label"] for option in table.values()]

        super().__init__(
            placeholder=menu["placeholder"],
            min_values=menu["min_values"],
            max_values=menu["max_values"],
            options=options
        )

    async def colour(self):
        '''
        Checks if the emote name already exists in the selected server
        '''
        if "Server" not in self.selection.keys():
            return config.colour["gold"]

        guild:Guild = self.selection["Server"]["guild"]
        emoji:list[Emoji] = await guild.fetch_emojis()
        names:list[str] = [emote.name for emote in emoji]
        selected:str = self.selection["Emote"]["emoji"].name

        if selected not in names:
            self.valid:bool = True
            return config.colour["green"]
        else:
            self.valid:bool = False
            return config.colour["red"]

    async def callback(self, interaction:Interaction):
        key:str = self.table[self.values[0]]["type"]
        self.selection[key] = self.table[self.values[0]]

        colour:str = await self.colour()

        embed = Embed(colour=colour)
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
                embed=embed,
                ephemeral=True
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
        self.selection:dict = selection
        self.responses:dict = responses
        options:list = [option["label"] for option in table.values()]

        super().__init__(
            placeholder=menu["placeholder"],
            min_values=menu["min_values"],
            max_values=menu["max_values"],
            options=options
        )

    async def colour(self):
        '''
        Checks to see if the selected guild has any vacant emote slots.
        '''
        guild:Guild = self.selection["Server"]["guild"]
        limit:int = guild.emoji_limit
        emoji:list[Emoji] = await guild.fetch_emojis()

        if len(emoji) <= limit:
            self.valid:bool = True
            return config.colour["green"]
        else:
            self.valid:bool = False
            return config.colour["red"]

    async def callback(self, interaction:Interaction):
        key:str = self.table[self.values[0]]["type"]
        self.selection[key] = self.table[self.values[0]]

        colour:str = await self.colour()

        embed = Embed(colour=colour)
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
                embed=embed,
                ephemeral=True
            )

class StealModal(Modal):
    def __init__(self, selection:dict, responses:dict):
        # Load modal configuration from JSON file
        modal_config:dict = config.load(
            path="commands/emotes/steal/modals/rename.json"
        )

        # Call the parent constructor and set the custom id
        super().__init__(
            title=modal_config["title"], 
            custom_id=modal_config["custom_id"]
        )

        # Reference the selection and response dictionaries from view
        self.responses:dict = responses
        self.selection:dict = selection

        # Modal for the user to rename the selected emote to
        self.rename:str = TextInput(
            label=modal_config["label"],
            placeholder=modal_config["placeholder"],
            required=modal_config["required"]
        )

        self.add_item(self.rename)

    async def on_submit(self, interaction:Interaction):
        # Changes the currently selected emote to the new name
        emoji:Emoji = self.selection["Emote"]["emoji"]
        emoji.name = self.rename.value

        # Interaction response to modal submission
        embed = Embed()
        embed.set_author(
            name="Emote"
        )
        embed.set_footer(
            text=self.rename.value, 
            icon_url=self.selection["Emote"]["url"]
        )

        # Modifies the Message object to the new selection
        await interaction.response.defer()
        await self.responses["Emote"].edit(embed=embed)