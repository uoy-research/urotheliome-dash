import pandas as pd
from db.connection import get_db_connection
from functools import lru_cache

@lru_cache(maxsize=32)
def fetch_gene_expression_data(selected_genes: tuple, selected_dataset: tuple) -> pd.DataFrame:
    """
    Fetch gene expression data with LRU caching.
    Args:
        selected_genes: Tuple of gene names
        selected_dataset: Tuple of dataset names
    Returns:
        DataFrame containing gene expression data
    """
    conn = get_db_connection()
    try:
        query = """
            SELECT 
                ge.GeneName,
                ge.TPM,
                s.DatasetName,
                s.SubsetName,
                s.TissueName,
                s.SubstrateType,
                s.Gender,
                s.Stage,
                s.Status,
                s.NhuDifferentiation,
                s.SampleId,
                s.TER
            FROM GeneExpression ge
            JOIN Sample s ON ge.SampleId = s.SampleId
            WHERE ge.GeneName IN ({})
            AND s.DatasetName IN ({})
        """.format(
            ', '.join(['?' for _ in selected_genes]),
            ', '.join(['?' for _ in selected_dataset])
        )
        
        # For large queries, use chunking
        if len(selected_genes) * len(selected_dataset) > 1000:
            chunks = []
            for chunk in pd.read_sql_query(
                query,
                conn,
                params=list(selected_genes) + list(selected_dataset),
                chunksize=10000
            ):
                chunks.append(chunk)
            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_sql_query(
                query,
                conn,
                params=list(selected_genes) + list(selected_dataset)
            )
        
        return df
    finally:
        conn.close()

# Helper function to clear the LRU cache
def clear_cache() -> None:
    fetch_gene_expression_data.cache_clear()
