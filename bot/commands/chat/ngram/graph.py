from pathlib import Path
import sys
# import numpy as np
# import asyncio

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model

class Graph():
    # CONSTRUCTOR::
    def __init__(self):
        self.model: Model = None
    
    @classmethod
    async def create(cls, database:str, script:str):
        self = cls()
        # Change ngram.db to main.db once feature is ready
        self.model = await Model.create(database=database, script=script)

        return self

    # GRAPH::
    async def words(self, string:str, n:int=1):
        '''
        Returns a list of all substrings where each substring is a sequence of n consecutive words.
        '''
        words: list[str] = string.split()
        n_words: list[list] = []

        for i in range(len(words)):
            if len(words[i:i+n]) >= n:
                sub_str: str = words[i:i+n]
                n_words.append(sub_str)

        return n_words

    async def add(self, string:str, union:int=1):
        '''
        Writes unique relationships to an SQL adjacency list
        '''
        n: int = union + 1
        slice_arr = await self.words(string=string, n=n)
        word_arr: list[str] = [" ".join(word) for word in slice_arr]

        # Insert or update new entries as new or unique and increments the edge
        for i, _ in enumerate(word_arr):
            prev_slice:list[str] = slice_arr[i-1][1-n:]
            curr_slice:list[str] = slice_arr[i][:n-1]
            curr:str = word_arr[i]
            prev:str = word_arr[i-1]

            if curr_slice == prev_slice:
                values:dict = {
                    "Current":curr, 
                    "Previous":prev,
                    "Edge":1,
                    }

                sql:str = """
                INSERT INTO Graph (Current, Previous, Edge)
                VALUES (:Current, :Previous, :Edge)
                ON CONFLICT (Current, Previous) DO UPDATE SET
                    Edge = Edge + 1;
                """
                await self.model.write(query=sql, values=values)

        # For each inserted or updated word, recalculate the probability
        for j, _ in enumerate(word_arr):
            prev_slice:list[str] = slice_arr[i-1][1-n:]
            curr_slice:list[str] = slice_arr[i][:n-1]
            curr:str = word_arr[j]
            prev:str = word_arr[j-1]

            if curr_slice == prev_slice:
                values:dict = {
                    "Current":curr,
                    "Previous":prev,
                }

                sql:str = """
                UPDATE Graph
                SET Probability = 
                    CAST(
                        (SELECT Edge FROM Graph WHERE Current = :Current AND Previous = :Previous) AS REAL) /
                        (SELECT SUM (Edge) FROM Graph WHERE Previous = :Previous)
                WHERE Current = :Current AND Previous = :Previous;
                """
                await self.model.write(query=sql, values=values)
        return

async def main():
    with open(file="the-velveteen-rabbit.txt") as file:
        text = file.read()
        graph = await Graph.create(database="main.db", script="ngram.sql")
        await graph.add(string=text, union=2)
        # sql = "SELECT * FROM Graph"
        # print(await graph.model.read(query=sql))
    return

if __name__ == "__main__":
    asyncio.run(main())