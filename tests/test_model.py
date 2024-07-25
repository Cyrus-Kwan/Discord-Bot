# PACKAGES::
import unittest
import asyncio
import pandas as pd
import pandas.testing as pdt

# ENVIRONMENT::
import sys
from pathlib import Path

PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
from models.model import Model

class TestModel(unittest.TestCase):
    model = Model("test_cases.db")

    async def test_read(self):
        # TEST CASE 1:: 
        data = {
            "id": [1, 2, 3, 4, 5], 
            "title": ["Deadpool & Wolverine", "Inside Out 2", "Fly Me to the Moon", "The Garfield Movie", "The Watchers"], 
            "release_date": ["2024-07-25", "2024-06-13", "2024-07-11", "2024-05-30", "2024-06-06"], 
            "score": [8, 9, 7, 5, 3],
            }
        expected = pd.DataFrame(data=data)
        sql = "SELECT * FROM movies"
        try:
            result = await self.model.select(sql)
            pdt.assert_frame_equal(result, expected)
        except AssertionError as e:
            self.fail(f"DataFrames are not equal: {e}")

        # TEST CASE 2::
        data = {
            "id": [1, 2, 3], 
            "title": ["Deadpool & Wolverine", "Inside Out 2", "Fly Me to the Moon"], 
            "release_date": ["2024-07-25", "2024-06-13", "2024-07-11"], 
            "score": [8, 9, 7],
            }
        expected = pd.DataFrame(data=data)
        sql = "SELECT * FROM movies WHERE score > 6;"
        try:
            result = await self.model.select(sql)
            pdt.assert_frame_equal(result, expected)
        except AssertionError as e:
            self.fail(f"DataFrames are not equal: {e}")

if __name__ == "__main__":
    unittest.main()