from dash import dcc

def gene_expression_plot():
    # This component will render the gene expression plot
    return dcc.Graph(id="gene-expression-plot")

def gene_comparison_plot():
    # Component for rendering the gene comparison scatter plot
    return dcc.Graph(id="gene-comparison-plot")
