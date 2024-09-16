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

from Libs.config import *

def load(path:str) -> dict:
    '''
    Returns config data from respective file path
    '''
    directory = pathlib.Path(__file__).parent
    config:str = f"{name(path=path)}.json"

    with open(directory / config) as f:
        data:dict = json.load(f)

    return data

def name(path:str) -> str:
    '''
    Takes a file path and returns the excluded file type substring
    '''
    # Retrieves the file name from given path
    file_path = pathlib.Path(path)
    file_name = file_path.name

    # Matches non-special characters until "."
    pattern:str = r"[^/\\.:*?<>]*(?=\.)"
    search:str = re.search(pattern=pattern, string=file_name).group()

    return search

def colour():
    colour:dict = {
        key:int(value, base=16) for key, value in load("colours.json").items()
    }

    return colour

def main():
    print(load(__file__))
    return

if __name__ == "__main__":
    main()