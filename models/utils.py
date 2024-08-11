# I/O COLOR MODIFICATIONS::
color = {
    "black":"\033[0;30m",
    "red":"\033[0;31m",
    "green":"\033[0;32m",
    "yellow":"\033[0;33m",
    "blue":"\033[0;34m",
    "purple":"\033[0;35m",
    "cyan":"\033[0;36m",
    "white":"\033[0;37m",
}

# SQL QUERY VALIDATION::
def sql_contains(query:str, keywords:set[str]) -> bool:
    '''
    Checks a given string whether or not a specific keyword or keywords in a set is present.
    '''
    if type(keywords) == str:
        if keywords in query:
            return True
        else:
            return False

    for keyword in keywords:
        if keyword in query.upper():
            return True
    return False

def main():
    sql = """
    -- Store basic user information WIP
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        server_name TEXT,
        global_name TEXT
    )
    """
    print(sql_contains(sql, {"INSERT", "UPDATE", "DELETE", "ALTER", "CREATE"}))

if __name__ == "__main__":
    main()