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

from Libs.commands.triggers import *

class Trigger:
    '''
    Event decorators for application commands
    '''
    def __init__(self, client:Client):
        self.client:Client = client
        self.event_commands:dict = {}

    def listen(self, event_name:str):
        # Add coroutine to event_commands when decorated as "name":[coroutine]
        def add_coro(func:Coroutine):
            if event_name in self.event_commands.keys():
                self.event_commands[event_name].append(func)
            else:
                self.event_commands[event_name] = [func]

        return add_coro

    def create(self, event_name:str):
        # Creates the event coroutine that will run all decorated commands
        async def event(*args, **kwargs):
            commands:list = []

            for command in self.event_commands[event_name]:
                commands.append(command(*args, **kwargs))

            await asyncio.gather(*commands)

        return event

    def register(self):
        # For each for each coroutine, register to the bot event as
        # client.name = name
        # e.g. client.on_ready = on_ready
        for event_name in self.event_commands.keys():
            setattr(
                self.client, event_name, self.create(event_name=event_name)
            )