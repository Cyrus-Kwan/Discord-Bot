# import re
# import asyncio
# import numpy as np
# from discord import Client
import sys
from pathlib import Path

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model

class NGram():
    # CONSTRUCTOR::
    def __init__(self, model:Model):
        self.model = model

    async def generate(self, start:str, stop:str, n:int=1000):
        last_word:str = start
        chain:list[str] = [start]
        guard:tuple = (None, stop)
        
        for _ in range(n):
            if last_word in guard:
                break

            sql:str = f"""
            SELECT Current, Probability FROM Graph WHERE Previous = :last_word;
            """
            values:dict[str] = {
                "last_word":last_word
                }
            next_choice:pd.DataFrame = await self.model.read(query=sql, values=values)

            # Handle when the last_word leads to dead end
            if next_choice.empty:
                break
            else:
                next_word:str = np.random.choice(next_choice["Current"], p=next_choice["Probability"])
                chain.append(next_word.split()[-1])
                last_word = next_word

        return " ".join(chain)

    async def short(self, string:str):
        pattern = r"[^\"\n]*?[.?!]"
        str_arr:list[str] = re.findall(pattern=pattern, string=string)
        choices:list[str] = []
        for text in str_arr:
            if text != '':
                choices.append(text)

        return np.random.choice(choices)

async def main():
    mod = await Model.create(database="ngram.db", script="ngram.sql")
    ngram = NGram(model=mod)
    gen = await ngram.generate(start="There was once", stop="to be Real.")
    print(await ngram.short(gen))
    # print(gen)
    return

if __name__ == "__main__":
    asyncio.run(main())