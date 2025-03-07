from dash import dcc
from data.fetch_names import fetch_gene_names

def gene_dropdown():
    gene_names = fetch_gene_names()  # Fetch the gene names from the database
    return dcc.Dropdown(
        id="gene-dropdown",
        options=[{"label": gene, "value": gene} for gene in gene_names],
        multi=True,
        placeholder="Select genes..."
    )

def xaxis_dropdown():
    options = [
        {"label": "Gene Name", "value": "GeneName"},
        {"label": "NHU", "value": "NhuDifferentiation"},
        {"label": "Tissue", "value": "TissueName"},
        {"label": "Gender", "value": "Gender"},
        {"label": "Substrate", "value": "SubstrateType"},
        {"label": "Dataset Subset", "value": "SubsetName"},
        {"label": "Tumor Stage", "value": "Stage"},
        {"label": "Vital Status", "value": "Status"}
    ]
    return dcc.Dropdown(
        id="xaxis-dropdown",
        options=options,
        value="GeneName",
        clearable=False,
        placeholder="Select X-axis..."
    )
