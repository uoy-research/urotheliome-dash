from dash import dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from data.fetch_names import fetch_gene_names

def gene_dropdown():
    gene_names = fetch_gene_names()  # Fetch the gene names from the database
    return dmc.MultiSelect(
        id="gene-dropdown",
        data=[{"label": gene, "value": gene} for gene in gene_names],
        searchable=True,
        limit=50,
        placeholder="Select genes...",
        clearable=True,
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
    return dmc.Select(
        id="xaxis-dropdown",
        data=options,
        value="GeneName",
        clearable=False,
        placeholder="Select X-axis...",
    )

def gene_comparison_dropdown_1():
    gene_names = fetch_gene_names()
    return dmc.Select(
        id="gene-comparison-dropdown-1",
        data=[{"label": gene, "value": gene} for gene in gene_names],
        searchable=True,
        limit=50,
        placeholder="Select first gene...",
        clearable=True,
    )

def gene_comparison_dropdown_2():
    gene_names = fetch_gene_names()
    return dmc.Select(
        id="gene-comparison-dropdown-2",
        data=[{"label": gene, "value": gene} for gene in gene_names],
        searchable=True,
        limit=50,
        placeholder="Select second gene...",
        clearable=True,
    )
