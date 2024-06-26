import pandas as pd
import numpy as np

data_path = "JBU_data/all_data.tsv"

metadata_path = "JBU_data/metadata_v3.tsv"

data_tpm = pd.read_csv(data_path, sep="\t")
metadata = pd.read_csv(metadata_path, sep="\t")

baker_metadata = metadata[metadata["Dataset"] == "Baker_BK"]

baker_tpm = data_tpm[["genes"] + list(baker_metadata["Sample"])]

baker_tpm = baker_tpm.dropna().set_index("genes")
baker_tpm.to_csv("data/gene_viz/baker_BK.tsv", sep="\t")

baker_metadata = baker_metadata.reset_index(drop=True)
baker_metadata.to_csv("data/gene_viz/meta_baker_BK.tsv", sep="\t")
