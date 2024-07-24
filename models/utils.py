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
def write_sql(query:str):
    write_sql = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"]
    for keyword in write_sql:
        if keyword in query.upper():
            return True
    return False

def read_sql(query:str):
    read_sql = ["SELECT"]
    for keyword in read_sql:
        if keyword in query.upper():
            return True
    return False

def main():
    sql = """
    SELECT * FROM sqlite_master WHERE type='table';
    """
    print(write_sql(sql))

if __name__ == "__main__":
    main()