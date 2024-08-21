from pathlib import Path
import sys
import numpy as np
import json
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

    async def adj_graph(self, string:str, union:int=1):
        '''
        Returns adjacency list that contains only the relationships between each state and the next
        '''
        n: int = union + 1
        slice_arr = await self.words(string=string, n=n)
        word_arr: list[str] = [" ".join(word) for word in slice_arr]
        # slice_arr: list[str] = words(string=string)

        graph: dict = {word:{} for word in word_arr}

        for i in range(len(word_arr)):
            prev_slice: list[str] = slice_arr[i-1][1-n:]
            curr_slice: list[str] = slice_arr[i][:n-1]
            curr: str = word_arr[i]
            prev: str = word_arr[i-1]

            if curr_slice == prev_slice:
                values: dict = {
                    "current":curr, 
                    "previous":prev,
                    }

                sql: str = """
                INSERT INTO graph (current, previous, edge)
                VALUES (:current, :previous, 0)
                ON CONFLICT (current, previous) DO UPDATE SET
                    edge = edge + 1;
                """
                await self.model.write(query=sql, values=values)

        # Try handling this functionality in sql
            if prev in graph[curr].keys():
                graph[curr][prev] += 1
            else:
                graph[curr][prev] = 1

        for curr in graph.keys():
            total = sum(graph[curr].values())
            for prev in graph[curr].keys():
                graph[curr][prev] = graph[curr][prev]/total

        return graph

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

    graph = await Graph.create()
    await graph.adj_graph(string=text, union=1)

    sql = "SELECT * FROM graph;"

    print(await graph.model.read(sql))

    return

if __name__ == "__main__":
    asyncio.run(main())