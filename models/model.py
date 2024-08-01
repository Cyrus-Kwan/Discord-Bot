# PACKAGES::
from pathlib import Path
import pandas as pd
import sqlite3
import sys
import asyncio
import re

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

# MODULES::
import models
from models import *

class Model():
    # Constructor
    def __init__(self, database:str):
        self.connection: sqlite3.Connection = self.database_connect(database)
        self.cursor: sqlite3.Connection.cursor = self.connection.cursor()
        self.schema: dict[pd.DataFrame] = None

    @classmethod
    async def create(cls, database:str, script:str=None):
        '''
        Asynchronous method for model creation.
        This should be called as 'obj = Model.create(database)' whenever a new model is created instead of 'obj = Model(database)'
        '''
        self = cls(database=database)
        if script:
            await self.inject(script)
        self.schema = await self.get_schema()

        return self

    # Initialization helpers::
    def database_connect(self, database:str) -> sqlite3.Connection:
        '''
        Creates a connection to the specified database file.
        '''
        database_dir: pathlib.WindowsPath = Path(__file__).parent / "databases"
        connection: sqlite3.Connection = sqlite3.connect(database_dir / database)

        return connection

    async def get_schema(self) -> dict[pd.DataFrame]:
        '''
        Returns the schema of the entire database as a map containing each table to their names.
        '''
        sql: str = "SELECT name FROM sqlite_master WHERE type='table';"
        selection: list[tuple] = self.cursor.execute(sql).fetchall()
        table: pd.DataFrame = await self.read(sql)
        table_names: pd.Series = table["name"]

        # Dictionary containing the tables in the database stored as pandas dataframes
        schema: dict[pd.DataFrame] = {}
        for table in table_names:
            sql = f"SELECT * FROM {table};"
            schema[table] = await self.read(sql)

        return schema

    # Database Operations::
    async def read(self, query:str) -> pd.DataFrame:
        '''
        Returns an SQL query as a pandas DataFrame object for simpler indexing.
        Ensures only SELECT queries are allowed and guards against SQL injection.
        '''
        if len(query.split(";")) > 2:
            # 2 covers both cases where the query does or doesn't end with a ';' character
            error_message = "Only a single query is allowed."
            raise ValueError(f"{utils.color['red']}{error_message}{utils.color['white']}")
            return None

        if not utils.sql_contains(query, {"SELECT"}):
            error_message = "Only SELECT queries are allowed."
            raise ValueError(f"{utils.color['red']}{error_message}{utils.color['white']}")
            return None

        with self.connection:
            columns: list[str] = []
            for value in self.cursor.execute(query).description:
                columns.append(value[0])

            sql = pd.read_sql_query(query, self.connection)
            select = pd.DataFrame(sql, columns=columns)

        return select

    async def write(self, query:str) -> None:
        '''
        Writes to an existing database using the given sql query.
        Ensures that 
        '''
        if len(query.split(";")) > 2:
            # 2 covers both cases where the query does or doesn't end with a ';' character
            error_message = "Only a single query is allowed."
            raise ValueError(f"{utils.color['red']}{error_message}{utils.color['white']}")
            return None

        if not utils.sql_contains(query, {"INSERT", "UPDATE", "DELETE", "ALTER", "CREATE"}):
            error_message = "Only 'ALTER', 'CREATE', 'INSERT', 'UPDATE', or 'DELETE' queries are allowed."
            raise ValueError(f"{utils.color['red']}{error_message}{utils.color['white']}")
            return None

        with self.connection:
            self.cursor.execute(query)
            self.connection.commit()

        self.schema = await self.get_schema()

        return None

    async def inject(self, script:str) -> None:
        '''
        Writes to a database using content from a given .sql file.
        '''
        if not re.search(r".sql$", script):
            error_message = "Expected .sql file."
            raise AttributeError(f"{utils.color['red']}{error_message}{utils.color['white']}")
            return None

        script_path = Path(*models.scripts.__path__)
        with open(f"{script_path}/{script}") as content:
            sql = content.read()
            for query in sql.split(";")[:-1]:
                await self.write(query)

        self.schema = await self.get_schema()

        return None

async def main():
    mod = await Model.create("test.db")
    # sql = """
    # INSERT INTO people (first_name, last_name, age, gender) VALUES
    # ('John', 'Snow', 34, 'm');
    # """
    # await mod.write(sql)

    # sql = """
    # SELECT * FROM people;
    # """
    # print(await mod.read(sql))

    # sql = """
    # DELETE FROM people WHERE first_name='John' AND last_name='Snow';
    # """
    # await mod.write(sql)

    print(mod.schema)
    await mod.inject("test_cases.sql")
    print(mod.schema)

if __name__ == "__main__":
    asyncio.run(main())