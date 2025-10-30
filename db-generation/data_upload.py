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

def load_metadata_tsv(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df

def insert_into_db(df, table_name, conn):
    #Insert a DataFrame (clean) into the specified SQLite table.
    try:
        df.to_sql(table_name, conn, if_exists='fail', chunksize=5000, index=False)
        print(f"Successfully populated {table_name}")
    except Exception as e:
        print(f"Error updating {table_name}: {e}")

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

# - Gene_Expression
# Drop columns if column name in {'TCGA-BL-A13I-01A', 'TCGA-BL-A13J-01A', 'TCGA-BL-A0C8-01A'}
# TODO what is this doing, and should it be done in metadata / raw data?
columns_to_drop = {'TCGA-BL-A13I-01A', 'TCGA-BL-A13J-01A', 'TCGA-BL-A0C8-01A'}
all_data_df.drop(columns=columns_to_drop, inplace=True)
df_long = all_data_df.melt(id_vars=["genes"], var_name="sample_id", value_name="TPM")
df_long.dropna(subset=["TPM"], inplace=True)
df_long = df_long.rename(columns={"genes": "GeneName", "sample_id": "SampleId"})
# Insert into db
# TODO shouldn't this be violating a FK constraint? I.e. adding TPM counts for
# samples but the Sample table hasn't been populated yet. Check again when have
# DB created from schema
insert_into_db(df_long, "GeneExpression", conn)

# - Gene
gene_df = all_data_df[['genes']].drop_duplicates().reset_index(drop=True)
gene_df = gene_df.rename(columns={"genes": "GeneName"})
# Insert into db
insert_into_db(gene_df, "Gene", conn)

# NHU
nhu_df = metadata_df[['NHU_differentiation']].drop_duplicates().reset_index(drop=True)
nhu_df = nhu_df.dropna()
# Remove '?' row
nhu_df = nhu_df[nhu_df['NHU_differentiation'] != '?']
nhu_df = nhu_df.rename(columns={"NHU_differentiation": "NhuDifferentiation"})
# Insert into db
insert_into_db(nhu_df, "NHU", conn)

# Dataset_Subset
dataset_subset_df = metadata_df[['subset_name']].drop_duplicates().reset_index(drop=True)
dataset_subset_df = dataset_subset_df.rename(columns={"subset_name": "SubsetName"})
# Insert into db
insert_into_db(dataset_subset_df, "DatasetSubset", conn)

# - Dataset
dataset_df = metadata_df[['Dataset']].drop_duplicates().reset_index(drop=True)
dataset_df = dataset_df.rename(columns={"Dataset": "DatasetName"})
# Insert into db
insert_into_db(dataset_df, "Dataset", conn)

# - Tissue
tissue_df = metadata_df[['Tissue']].drop_duplicates().reset_index(drop=True)
tissue_df = tissue_df.rename(columns={"Tissue": "TissueName"})
# Insert into db
insert_into_db(tissue_df, "Tissue", conn)

# - Substrate
substrate_df = metadata_df[['Substrate']].drop_duplicates().reset_index(drop=True)
# Remove nan
substrate_df = substrate_df.dropna()
# Remove '?' row
substrate_df = substrate_df[substrate_df['Substrate'] != '?']
substrate_df = substrate_df.rename(columns={"Substrate": "SubstrateType"})
# Insert into db
insert_into_db(substrate_df, "Substrate", conn)

# - Gender
gender_df = metadata_df[['Gender']].drop_duplicates().reset_index(drop=True)
# remove nan
gender_df = gender_df.dropna()
# Insert into db
insert_into_db(gender_df, "Gender", conn)

# - Tumor_Stage
tumor_stage_df = metadata_df[['tumor_stage']].drop_duplicates().reset_index(drop=True)
tumor_stage_df = tumor_stage_df.dropna()
tumor_stage_df = tumor_stage_df.rename(columns={"tumor_stage": "Stage"})
# Insert into db
insert_into_db(tumor_stage_df, "TumorStage", conn)

# - Vital_Status
vital_status_df = metadata_df[['vital_status']].drop_duplicates().reset_index(drop=True)
vital_status_df = vital_status_df.dropna()
vital_status_df = vital_status_df.rename(columns={"vital_status": "Status"})
# Insert into db
insert_into_db(vital_status_df, "VitalStatus", conn)

# - Sample
metadata_df.replace({'?': None, 'NaN': None, '': None}, inplace=True)
metadata_df = metadata_df.where(pd.notna(metadata_df), None)  # Convert all NaNs to None
# Remove unnecessary columns
metadata_df.drop(columns=["shared_num_same_col", "CCL_relatedness", "CCL_tissue_origin", "Diagnosis", 'incl_ABS-Ca_diff_Bladder',
       'incl_ABS-Ca_diff_healthy_Bladder', 'incl_ABS-Ca_diff_Ureter',
       'incl_undiff_Bladder', 'incl_undiff_healthy_Bladder',
       'incl_undiff_Ureter', 'incl_P0_Bladder', 'incl_P0_healthy_Bladder',
       'incl_P0_Ureter','TCGA408_classifier', 'MIBC_2019CC', 'MIBC_2019CC-noSR'], inplace=True)
# Rename columns
metadata_df.rename(columns={"Sample": "SampleId", "subset_name": "SubsetName", "Dataset": "DatasetName", "Tissue": "TissueName", "Substrate": "SubstrateType", "Gender": "Gender", "tumor_stage": "Stage", "vital_status": "Status", "NHU_differentiation": "NhuDifferentiation", "TER": "TER", "days_to_death": "DaysToDeath"}, inplace=True)
# Insert into db
insert_into_db(metadata_df, "Sample", conn)

# Create indexes for faster querying
# Rename to PascalCase
cursor.execute("CREATE INDEX IF NOT EXISTS IdxGeneExpressionGeneName ON GeneExpression(GeneName);")
print("created index for GeneName")
cursor.execute("CREATE INDEX IF NOT EXISTS IdxSampleDatasetName ON Sample(DatasetName);")
print("created index for Sample")

# Save changes
conn.commit()
conn.close()
