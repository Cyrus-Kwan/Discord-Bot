# PACKAGES::
from pathlib import Path
import pandas as pd
import sqlite3
import sys

# ENVIRONMENT::
PYTHONPATH = Path(__file__).parents[1].__str__()
if PYTHONPATH not in sys.path:
    sys.path.append(PYTHONPATH)

from models import *

class Model():
    def __init__(self, database:str):
        self.connection: sqlite3.Connection = self.database_connect(database)
        self.cursor: sqlite3.Connection.cursor = self.connection.cursor()
        self.schema: set[pd.DataFrame] = self.get_schema()

# Initialization helpers::
    def database_connect(self, database:str) -> sqlite3.Connection:
        '''
        Creates a connection to the specified database file.
        '''
        database_dir: pathlib.WindowsPath = Path(__file__).parent / "databases"
        connection: sqlite3.Connection = sqlite3.connect(database_dir / database)

        return connection

    def get_schema(self) -> dict[pd.DataFrame]:
        '''
        Returns the schema of the entire database as a map containing each table to their names.
        '''
        sql: str = "SELECT name FROM sqlite_master WHERE type='table';"
        selection: list[tuple] = self.cursor.execute(sql).fetchall()
        table_names: pd.DataFrame = self.select(sql)["name"]

        # Dictionary containing the tables in the database stored as pandas dataframes
        schema: dict[pd.DataFrame] = {}
        for table in table_names:
            sql = f"SELECT * FROM {table};"
            schema[table] = self.select(sql)

        return schema

# Database Operations::
    def select(self, query:str) -> pd.DataFrame:
        '''
        Returns an SQL query as a pandas DataFrame object for simpler indexing.
        Ensures only SELECT queries are allowed and guards against SQL injection.
        '''
        if len(query.split(";")) > 2:
            # 2 covers both cases where the query does or doesn't end with a ';' character
            error_message = "Only a single query is allowed."
            raise ValueError(f"{utils.color['red']}{error_message}{utils.color['white']}")

        if utils.write_sql(query):
            error_message = "Only SELECT queries are allowed."
            raise ValueError(f"{utils.color['red']}{error_message}{utils.color['white']}")

        with self.connection:
            columns: list[str] = []
            for value in self.cursor.execute(query).description:
                columns.append(value[0])

            sql = pd.read_sql_query(query, self.connection)
            selection = pd.DataFrame(sql, columns=columns)

        return selection

def main():
    mod = Model("test_cases.db")
    sql = """
    INSERT INTO people (first_name, last_name, age, gender) VALUES
    ('John', 'Snow', 34, 'm')
    """
    mod.select(sql)
    print(mod.schema["people"])

if __name__ == "__main__":
    main()