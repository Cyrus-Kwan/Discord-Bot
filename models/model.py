from pathlib import Path
import pandas as pd
import sqlite3

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

    def select(self, query:str) -> pd.DataFrame:
        '''
        Returns an sql query as a pandas dataframe object for simpler indexing.
        '''
        columns = []
        for value in self.cursor.execute(query).description:
            columns.append(value[0])

        sql = pd.read_sql_query(query, self.connection)
        selection = pd.DataFrame(sql, columns=columns)
        return selection

def main():
    mod = Model("bot_config.db")
    print(mod.schema["bot_config"][mod.schema["bot_config"]["bot_name"] == "cmd#7080"]["access_token"])

if __name__ == "__main__":
    main()