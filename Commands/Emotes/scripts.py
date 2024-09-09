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

class EmoteScript:
    def __init__(self, file:str, name:str):
        self.script_config:dict = config.load(path=file)[name]["scripts"]

    def content(self, message:str):
        emote_pattern:str = self.script_config["emote_pattern"]
        name_pattern:str = self.script_config["name_pattern"]
        code_pattern:str = self.script_config["code_pattern"]
        emote_search:list[str] = re.findall(
            pattern=pattern, string=message.content
        )

        emotes:dict[str] = {}
        for emote in emote_search:
            name_search:str = re.search(
                pattern=name_pattern, string=emote
            ).group()
            code_search:str = re.search(
                pattern=code_pattern, string=emote
            ).group()

            url:str = self.script_config["url"].format(code=code_search)
            image:str = requests.get(url=url)
            emotes[name] = image

        return emotes