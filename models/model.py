# ENVIRONMENT SETUP::
import sys
import pathlib

PARENTPATH = "Discord Bot 3.0"
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

from Config import config
from Libs.models import *

class Model:
    def __init__(self, db_name:str):
        self.con:Connection = self.db_connect(db_name)
        self.cur:Cursor = self.con.cursor()

    @classmethod
    async def create(cls, db_name:str, query:str=None):
        '''
        Asynchronous method for model creation.
        This should be called as 'obj = Model.create(database)' 
        whenever a new model is created instead of 'obj = Model(database)'
        '''        
        
        self = cls(db_name=db_name)
        
        if query:
            self.cur.execute(query=query)

        return self

    def db_connect(self, db_name:str) -> Connection:
        '''
        Connects to the specified database
        Creates a new database if none exists
        '''
        cfg_data:dict = config.load(__file__)
        curr_dir:str = pathlib.Path(__file__).parent
        data_dir:str = cfg_data["directory"]
        database:str = curr_dir / data_dir / db_name

        con:Connection = sqlite3.connect(database=database)
        return conn

async def main():
    model = Model("test.db")
    return

if __name__ == "__main__":
    asyncio.run(main())