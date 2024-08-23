from pathlib import Path
import sys
import numpy as np
import asyncio

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[4].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model

class Graph():
    # CONSTRUCTOR::
    def __init__(self):
        self.model: Model = None
    
    @classmethod
    async def create(cls):
        self = cls()
        # Change ngram.db to main.db once feature is ready
        self.model = await Model.create(database="ngram.db", script="ngram.sql")

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
    text = """
        This is the house that Jack built. 
        This is the malt 
        That lay in the house that Jack built. 
        This is the rat, 
        That ate the malt 
        That lay in the house that Jack built. 
        This is the cat 
        That killed the rat, 
        That ate the malt 
        That lay in the house that Jack built. 
    """
    from datetime import datetime

    start = datetime.now()
    # with open(file="./the-velveteen-rabbit.txt", mode="r") as file:
        # text = file.read()
    graph = await Graph.create()
    await graph.add(string=text, union=1)

    stop = datetime.now() - start
    print(stop)

    # sql = """
    # SELECT
    #     CAST ((SELECT Edge FROM Graph WHERE Current = 'the rat,' AND Previous = 'is the') AS REAL)/
    #     (SELECT SUM(Edge) FROM Graph WHERE Previous = 'is the') AS ratio;"""
    sql = "SELECT * FROM Graph;"
    print(await graph.model.read(sql))

    return

if __name__ == "__main__":
    asyncio.run(main())