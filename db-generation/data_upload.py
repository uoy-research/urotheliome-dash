# Copy-paste of import_data.ipynb with some edits

# WORKS ON EMPTY DATABASE
import argparse
import os
import pandas as pd
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("db_path", type=str,
                    help="path to the database")
parser.add_argument("metadata_file_path", type=str,
                    help="path to the metadata file")
parser.add_argument("data_folder_path", type=str,
                    help="path to the data folder")
args = parser.parse_args()

# Connect to the existing SQLite database
db_path = args.db_path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON;")

def prepare_dimension_table(values, name, vals_to_remove=['?']):
    """
    Prepares a dimension table for the DB.

    The dimension tables are the tables that store a single property and are
    linked by foreign key to the main fact table (Sample in this instance).
    All of these tables are processed in typically the same way with a lot of
    duplicated code.

    In particular the steps are:

          - Obtain the unique values
          - Reset index
          - Remove missing values
          - Rename columns

    Args:
        - values (pandas.Series): A pandas series of all the raw values.
        - name (str): The new column name.
        - vals_to_remove (list[str]): List of values to remove.

    Returns:
        A pandas DataFrame with duplicate values removed.
    """
    df = (
        pd.DataFrame({ name: values })
        .drop_duplicates()
        .dropna()
        .reset_index(drop=True)
    )
    if len(vals_to_remove) > 0:
        df = df.loc[~df[name].isin(vals_to_remove)]

    return df


def insert_into_db(df, table_name, conn):
    #Insert a DataFrame (clean) into the specified SQLite table.
    df.to_sql(table_name, conn, if_exists='append', chunksize=5000, index=False)
    print(f"Successfully populated {table_name}")


def create_dimension(values, table_name, column_name, conn, vals_to_remove=['?']):
    """
    Creates a dimension table in the DB.

    Takes a list of raw values and processes it into a format that is expected
    by the DB scheme. In particular it finds the unique values, removes missing
    or other unsupported characters, and sets the appropriate column names.

    Args:
        - values (pandas.Series): A pandas series of all the raw values.
        - table_name (str): Name of the table to create.
        - column_name (str): The new column name.
        - conn (sqlite3.connection): Handle to an SQLite3 DB connection.
        - vals_to_remove (list[str]): List of values to remove.

    Returns:
        None, populates a table in the DB as a side-effect.
    """
    df_clean = prepare_dimension_table(values, column_name, vals_to_remove)
    insert_into_db(df_clean, table_name, conn)


def load_metadata_tsv(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df


def merge_all_datasets(base_path):
    first_file = True

    # Rather than incrementally joining each dataset, could read all datasets
    # into a list and then combine in 1 call:
    # pd.concat([x.set_index('genes') for x in dfs], axis=1).reset_index()
    # However, this has 2 downsides: 1) would require all data to fit into
    # memory, and 2) requires that the gene column is called 'genes', rather
    # than the more flexible requirement that gene names are in the first column
    for filename in os.listdir(base_path):
        # Exclude metadata files
        if "metadata" in filename:
            continue

        df = pd.read_csv(os.path.join(base_path, filename), delimiter="\t")
        print(f"Dataset: {filename} Shape {df.shape}")

        if first_file:
            all_tsv = df
            first_file = False
        else:
            # For gene expression data, merge on the gene column (first column)
            # Assuming first column contains gene names (usually 'genes')
            gene_col = df.columns[0]
            all_tsv = pd.merge(all_tsv, df, on=gene_col, how="outer")

    return all_tsv

def chunked_melt(df, id_vars, var_name, value_name, chunk_size):
    """
    Chunked melt operation to save memory usage.

    Args:
        - df (pd.DataFrame): DataFrame to melt.
        - id_vars (List[str]): As in pandas.melt.
        - var_name (str): As in pandas.melt.
        - value_name (str): As in pandas.melt.
        - chunk_size (int): Number of rows to pivot at a time.

    Returns:
        A pd.DataFrame of the combined long datasets.
    """
    chunked_res = []
    chunk_size = 100000

    for i in range(0, df.shape[0], chunk_size):
        chunked_df = df.iloc[i:i+chunk_size]
        chunked_df_long = chunked_df.melt(
            id_vars=id_vars,
            var_name=var_name,
            value_name=value_name
        )
        chunked_df_long.dropna(subset=["TPM"], inplace=True)
        chunked_res.append(chunked_df_long)

    return pd.concat(chunked_res)

# Load all data
all_data_df = merge_all_datasets(args.data_folder_path)
metadata_df = load_metadata_tsv(args.metadata_file_path)

# Convert all columns except first ('genes') to numeric, setting invalid values
# to NaN
all_data_df.iloc[:, 1:] = all_data_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Order of table creation + population
# - NHU
# - Dataset_Subset
# - Dataset
# - Tissue
# - Substrate
# - Gender
# - Tumor_Stage
# - Vital_Status
# - Gene
# - Sample
# - Gene_Expression

# Gene
create_dimension(all_data_df['genes'], 'Gene', 'GeneName', conn)

# NHU
create_dimension(
    metadata_df['NHU_differentiation'],
    'NHU',
    'NhuDifferentiation',
    conn
)

# Dataset_Subset
create_dimension(
    metadata_df['subset_name'],
    'DatasetSubset',
    'SubsetName',
    conn
)

# Dataset
create_dimension(
    metadata_df['Dataset'],
    'Dataset',
    'DatasetName',
    conn
)

# Tissue
create_dimension(
    metadata_df['Tissue'],
    'Tissue',
    'TissueName',
    conn
)

# Substrate
create_dimension(
    metadata_df['Substrate'],
    'Substrate',
    'SubstrateType',
    conn
)

# Gender
create_dimension(
    metadata_df['Gender'],
    'Gender',
    'Gender',
    conn
)

# Tumor_Stage
create_dimension(
    metadata_df['tumor_stage'],
    'TumorStage',
    'Stage',
    conn
)

# Vital_Status
create_dimension(
    metadata_df['vital_status'],
    'VitalStatus',
    'Status',
    conn
)

# Sample
# Restrict to columns of interest
metadata_cols = [
    ("Sample", "SampleId"),
    ("subset_name", "SubsetName"),
    ("Dataset", "DatasetName"),
    ("Tissue", "TissueName"),
    ("Substrate", "SubstrateType"),
    ("Gender", "Gender"),
    ("tumor_stage", "Stage"),
    ("vital_status", "Status"),
    ("NHU_differentiation", "NhuDifferentiation"),
    ("TER", "TER"),
    ("days_to_death", "DaysToDeath")
]
metadata_df = metadata_df[[x[0] for x in metadata_cols]]
metadata_df.rename(columns={ x[0]: x[1] for x in metadata_cols }, inplace=True)
# Clean error codes and missingness
metadata_df.replace({'?': None, 'NaN': None, '': None}, inplace=True)
metadata_df = metadata_df.where(pd.notna(metadata_df), None)
# Insert into db
insert_into_db(metadata_df, "Sample", conn)

# Gene_Expression
df_long = chunked_melt(
    all_data_df,
    id_vars=['genes'],
    var_name='sample_id',
    value_name='TPM',
    chunk_size=5000
)

df_long = df_long.rename(columns={"genes": "GeneName", "sample_id": "SampleId"})
# Restrict gene data to sample ids that are in the metadata
df_long = df_long.loc[df_long['SampleId'].isin(metadata_df['SampleId'].unique())]
insert_into_db(df_long, "GeneExpression", conn)

# Create indexes for faster querying
# Rename to PascalCase
cursor.execute("CREATE INDEX IF NOT EXISTS IdxGeneExpressionGeneName ON GeneExpression(GeneName);")
print("created index for GeneName")
cursor.execute("CREATE INDEX IF NOT EXISTS IdxSampleDatasetName ON Sample(DatasetName);")
print("created index for Sample")

# Save changes
conn.commit()
conn.close()
