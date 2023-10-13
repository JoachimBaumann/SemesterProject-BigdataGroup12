import sqlite3
from typing import Dict, List, Tuple

def get_table_info(db_path: str) -> Dict[str, Dict[str, str]]:
    """
    Get information about tables in an SQLite database.

    :param db_path: Path to the SQLite database.
    :return: A dictionary with table names as keys and another dictionary of {column_name: data_type} as values.
    """
    info = {}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        info[table_name] = {col[1]: col[2] for col in columns}

    conn.close()

    return info


# Example usage:
db_path = "datasets/taxi_dataset/2019/2019-01.sqlite"
# print(get_table_info(db_path))
