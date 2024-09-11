print("Importing bot dependencies...")

# Packages
import asyncio
import discord
from discord import Embed
from discord import Intents
from discord import Message
from discord import Interaction
from discord import app_commands
from discord.app_commands import CommandTree

# Modules
from Config import config
from Commands.Interface.interface import *
from Commands.Emotes.emotes import *