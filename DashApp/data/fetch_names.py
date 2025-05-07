from db.connection import get_db_connection
import pandas as pd

def fetch_gene_names():
    conn = get_db_connection()
    query = "SELECT GeneName FROM Gene"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df["GeneName"].tolist()

def fetch_datasets():
    conn = get_db_connection()
    query = "SELECT DatasetName FROM Dataset"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df["DatasetName"].tolist()
