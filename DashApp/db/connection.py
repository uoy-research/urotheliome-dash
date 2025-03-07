import sqlite3

DATABASE_PATH = "./urotheliome_data_indexed.db"
DATABASE_PATH_TEST = "./UrotheliomeData.db"

def get_db_connection() -> sqlite3.Connection:
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH_TEST)
    return conn
