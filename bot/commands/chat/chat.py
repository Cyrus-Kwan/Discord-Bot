import discord

class Chat():
    '''
    Functionality to send model-generated messages in response to a user interaction or certain prompts.
    '''
    # CONSTRUCTOR::
    def __init__(self, client:Client):
        self.client: Client = client
        self.tree: discord.Client.CommandTree = client.tree

    @classmethod
    async def register(cls, client:Client):
        self = cls(client=client)

        # Setup table for message logging
        await self.client.model.inject("messages.sql")

        # Register commands
        self.slash_commands()
        self.event_commands()

        return self

    # COMMANDS::
    def slash_commands(self):
        @self.tree.command(name="chat", description="Sends a generated message into the same channel the method was called.")
        async def chat(interaction:discord.Interaction) -> None:
            await interaction.response.send_message()
            return

    def event_commands(self):
        @self.client.event
        async def on_mention(message:discord.Message) -> None:
            await interaction.response.send_message()
            return