# Copy-paste of import_data.ipynb with some edits 

# WORKS ON EMPTY DATABASE
# 3 SAMPLES ARE MISSING FROM METADATA BUT EXIST IN ALL_DATA - THEY HAVE BEEN DROPPED

import sqlite3
import pandas as pd
import argparse

import os
print(os.getcwd())

parser = argparse.ArgumentParser()
parser.add_argument("db_path", type=str,
                    help="path to the database")
parser.add_argument("metadata_file_path", type=str,
                    help="path to the metadata file")
parser.add_argument("data_folder_path", type=str,
                    help="path to the data folder")
args = parser.parse_args()

# Connect to the existing SQLite database
#db_path = "../DashApp/data/script_test/UrotheliomeDataScriptTest.db"
db_path = args.db_path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON;")

#metadata_file_path = "../DashApp/data/script_test/metadata_v4.tsv"
metadata_file_path = args.metadata_file_path
#all_data_file_path = "../DashApp/data/script_test/all_data_test.tsv"

def load_metadata_tsv(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df

def load_all_data_tsv(file_path):
    df = pd.read_csv(file_path, sep='\t', low_memory=True)
    return df

def insert_into_db(df, table_name, conn):
    #Insert a DataFrame (clean) into the specified SQLite table.
    try:
        df.to_sql(table_name, conn, if_exists='replace', chunksize=10000,index=False)
        print(f"Successfully updated {table_name} with new data")
    except Exception as e:
        print(f"Error updating {table_name}: {e}")
        
def merge_all_datasets(base_path):
    #Merges all datasets from master.tsv and saves as all_data_test.tsv
    master_cv = pd.read_csv(base_path + "master.tsv", delimiter="\t")
    
    all_tsv = pd.DataFrame()
    for _, row in master_cv.iterrows():
        filename, _ = row["Filename"], row["Description"]
        df = pd.read_csv(base_path + filename, delimiter="\t")
        print("Dataset: {} Shape {}".format(filename, df.shape))

        # Exclude metadata file
        if "metadata" not in filename:
            if not all_tsv.empty:
                # For gene expression data, merge on the gene column (first column)
                # Assuming first column contains gene names
                gene_col = df.columns[0]  # Usually 'genes' or similar
                all_tsv = pd.merge(all_tsv, df, on=gene_col, how="outer")
            else:
                all_tsv = df
    print('completed merging')
    
    print(f"Final merged dataset shape: {all_tsv.shape}")

    # Uncomment to save as .tsv
    all_tsv.to_csv(base_path + "all_data_test.tsv", sep="\t", index=False)
    
    return all_tsv

# currently equivalent to all_data.tsv but depends on master.tsv file contents
#merged_df = merge_all_datasets("../DashApp/data/script_test/")
merged_df = merge_all_datasets(args.data_folder_path)

metadata_df = load_metadata_tsv(metadata_file_path)
#all_data_df = load_all_data_tsv(all_data_file_path)
all_data_df = merged_df

# Cleaning all_data_df
#print(all_data_df.info())
#print(all_data_df.dtypes)

# Convert all columns except 'gene' to numeric, setting errors='coerce' to convert invalid values to NaN
all_data_df.iloc[:, 1:] = all_data_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
missing_values_count = all_data_df.iloc[:, 1:].isnull().sum().sum()
print(f"\nTotal NaN values found in expression data: {missing_values_count}")

# Find rows where 'TCGA-ZF-AA56-01A' column has missing values
missing_rows = all_data_df[all_data_df['TCGA-ZF-AA56-01A'].isnull()]

# Find names of all genes (rows) with missing values
missing_genes = all_data_df[all_data_df.isnull().any(axis=1)]['genes'].tolist()

# Create a DataFrame of gene | number of samples with missing TPM value
missing_tpm_counts = all_data_df.isnull().sum(axis=1).reset_index()
missing_tpm_counts.columns = ['index', 'missing_count']
missing_tpm_counts = missing_tpm_counts[missing_tpm_counts['missing_count'] > 0]
missing_tpm_counts = missing_tpm_counts.merge(all_data_df[['genes']], left_on='index', right_index=True)
missing_tpm_counts = missing_tpm_counts[['genes', 'missing_count']]
#missing_tpm_counts

#all_data_df[all_data_df['TCGA-ZF-AA56-01A'].isnull()]

categorical_columns = ["subset_name", "Dataset", "Tissue", "NHU_differentiation", 
                       "Substrate", "Gender", "tumor_stage", "vital_status"]
#for col in categorical_columns:
    #print(f"Unique values in {col}:")
    #print(metadata_df[col].unique(), "\n")

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
#all_data_df
# Drop columns if column name in {'TCGA-BL-A13I-01A', 'TCGA-BL-A13J-01A', 'TCGA-BL-A0C8-01A'}
columns_to_drop = {'TCGA-BL-A13I-01A', 'TCGA-BL-A13J-01A', 'TCGA-BL-A0C8-01A'}
all_data_df.drop(columns=columns_to_drop, inplace=True)
print("dropped columns")
#all_data_df
print(all_data_df.shape)
df_long = all_data_df.melt(id_vars=["genes"], var_name="sample_id", value_name="TPM")
print("melted")
#df_long
df_long.dropna(subset=["TPM"], inplace=True)
print("dropped na")
df_long = df_long.rename(columns={"genes": "GeneName", "sample_id": "SampleId"})
print("columns renamed")
#df_long
# Insert into db
insert_into_db(df_long, "GeneExpression", conn)
print("end of expression statement")

# - Gene
gene_df = all_data_df[['genes']].drop_duplicates().reset_index(drop=True)
gene_df = gene_df.rename(columns={"genes": "GeneName"})
#gene_df
# Insert into db
insert_into_db(gene_df, "Gene", conn)

# NHU
nhu_df = metadata_df[['NHU_differentiation']].drop_duplicates().reset_index(drop=True)
nhu_df = nhu_df.dropna()
# Remove '?' row
nhu_df = nhu_df[nhu_df['NHU_differentiation'] != '?']
nhu_df = nhu_df.rename(columns={"NHU_differentiation": "NhuDifferentiation"})
#nhu_df
# Insert into db
insert_into_db(nhu_df, "NHU", conn)

# Dataset_Subset
dataset_subset_df = metadata_df[['subset_name']].drop_duplicates().reset_index(drop=True)
dataset_subset_df = dataset_subset_df.rename(columns={"subset_name": "SubsetName"})
#print(dataset_subset_df.to_string())
# Insert into db
insert_into_db(dataset_subset_df, "DatasetSubset", conn)

# - Dataset
dataset_df = metadata_df[['Dataset']].drop_duplicates().reset_index(drop=True)
dataset_df = dataset_df.rename(columns={"Dataset": "DatasetName"})
#dataset_df
# Insert into db
insert_into_db(dataset_df, "Dataset", conn)

# - Tissue
tissue_df = metadata_df[['Tissue']].drop_duplicates().reset_index(drop=True)
tissue_df = tissue_df.rename(columns={"Tissue": "TissueName"})
#tissue_df
# Insert into db
insert_into_db(tissue_df, "Tissue", conn)

# - Substrate
substrate_df = metadata_df[['Substrate']].drop_duplicates().reset_index(drop=True)
# Remove nan
substrate_df = substrate_df.dropna()
# Remove '?' row
substrate_df = substrate_df[substrate_df['Substrate'] != '?']
substrate_df = substrate_df.rename(columns={"Substrate": "SubstrateType"})
#substrate_df
# Insert into db
insert_into_db(substrate_df, "Substrate", conn)

# - Gender
gender_df = metadata_df[['Gender']].drop_duplicates().reset_index(drop=True)
# remove nan
gender_df = gender_df.dropna()
#gender_df
# Insert into db
insert_into_db(gender_df, "Gender", conn)

# - Tumor_Stage
tumor_stage_df = metadata_df[['tumor_stage']].drop_duplicates().reset_index(drop=True)
tumor_stage_df = tumor_stage_df.dropna()
tumor_stage_df = tumor_stage_df.rename(columns={"tumor_stage": "Stage"})
#tumor_stage_df
# Insert into db
insert_into_db(tumor_stage_df, "TumorStage", conn)

# - Vital_Status
vital_status_df = metadata_df[['vital_status']].drop_duplicates().reset_index(drop=True)
vital_status_df = vital_status_df.dropna()
vital_status_df = vital_status_df.rename(columns={"vital_status": "Status"})
#vital_status_df
# Insert into db
insert_into_db(vital_status_df, "VitalStatus", conn)

# - Sample
metadata_df.replace({'?': None, 'NaN': None, '': None}, inplace=True)
metadata_df = metadata_df.where(pd.notna(metadata_df), None)  # Convert all NaNs to None
metadata_df.shape
metadata_df.columns
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
#metadata_df

# Create indexes for faster querying
# Rename to PascalCase
cursor.execute("CREATE INDEX IF NOT EXISTS IdxGeneExpressionGeneName ON GeneExpression(GeneName);")
print("created index for GeneName")
cursor.execute("CREATE INDEX IF NOT EXISTS IdxSampleDatasetName ON Sample(DatasetName);")
print("created index for Sample")

# Save changes
conn.commit()

cursor.execute("SELECT COUNT(*) FROM GeneExpression")
print("selected count(*) from gene expression")
row_count = cursor.fetchone()[0]
print(f"Total rows in GeneExpression: {row_count}")

# Fix SubsetName mappings for specific samples to ensure one-to-one mapping
# Y2384-D should be changed to Uro-D (from whatever it currently is)
# Y2383-P0 should be changed to Uro-P0 (from whatever it currently is)
# This maintains historical SubsetName mapping as discussed
print("Before correction - checking current SubsetName values:")
cursor.execute("SELECT SampleId, SubsetName FROM Sample WHERE SampleId IN ('Y2384-D', 'Y2383-P0')")
current_values = cursor.fetchall()
for sample_id, subset_name in current_values:
    print(f"  {sample_id}: {subset_name}")
# Apply the corrections
corrections_made = 0
# Update Y2384-D to Uro-D
cursor.execute("UPDATE Sample SET SubsetName = 'Uro-D' WHERE SampleId = 'Y2384-D'")
if cursor.rowcount > 0:
    corrections_made += 1
    print(f"✓ Updated Y2384-D SubsetName to 'Uro-D'")
# Update Y2383-P0 to Uro-P0  
cursor.execute("UPDATE Sample SET SubsetName = 'Uro-P0' WHERE SampleId = 'Y2383-P0'")
if cursor.rowcount > 0:
    corrections_made += 1
    print(f"✓ Updated Y2383-P0 SubsetName to 'Uro-P0'")
print(f"\nTotal corrections applied: {corrections_made}")
print("\nAfter correction - verifying updated values:")
cursor.execute("SELECT SampleId, SubsetName FROM Sample WHERE SampleId IN ('Y2384-D', 'Y2383-P0')")
updated_values = cursor.fetchall()
for sample_id, subset_name in updated_values:
    print(f"  {sample_id}: {subset_name}")
# Commit the changes
conn.commit()
print("\n✓ SubsetName corrections committed to database")

# Close without saving changes
conn.close()

