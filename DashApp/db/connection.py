import sqlite3
import os

#DATABASE_PATH = "./UrotheliomeData.db"
DATABASE_PATH = os.getenv('DATABASE_PATH') or "'../data/UrotheliomeData.db'"

def get_db_connection() -> sqlite3.Connection:
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn
