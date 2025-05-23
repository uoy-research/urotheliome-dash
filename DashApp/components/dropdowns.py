from dash import dcc
import dash_bootstrap_components as dbc
from data.fetch_names import fetch_gene_names

# TODO - fetch from database every time or store in memory? fetch from database (potential easier updates), mermory should be faster. 
# Could restart docker container whenever a new dataset is added and then fetch from memory?
# Fetch gene names once rather than every time the dropdown is called?

def gene_dropdown():
    gene_names = fetch_gene_names()  # Fetch the gene names from the database
    return dcc.Dropdown(
        id="gene-dropdown",
        options=[{"label": gene, "value": gene} for gene in gene_names],
        multi=True,
        placeholder="Select genes...",
        className="dbc"
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
        {"label": "Vital Status", "value": "Status"},
        {"label": "Sample ID", "value": "SampleId"},
        {"label": "TER", "value": "TER"}
    ]
    return dcc.Dropdown(
        id="xaxis-dropdown",
        options=options,
        value="GeneName",
        clearable=False,
        placeholder="Select X-axis...",
        className="dbc"
    )

def gene_comparison_dropdown_1():
    gene_names = fetch_gene_names()
    return dcc.Dropdown(
        id="gene-comparison-dropdown-1",
        options=[{"label": gene, "value": gene} for gene in gene_names],
        placeholder="Select first gene...",
        className="dbc"
    )

def gene_comparison_dropdown_2():
    gene_names = fetch_gene_names()
    return dcc.Dropdown(
        id="gene-comparison-dropdown-2",
        options=[{"label": gene, "value": gene} for gene in gene_names],
        placeholder="Select second gene...",
        className="dbc"
    )
