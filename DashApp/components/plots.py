from dash import dcc

def gene_expression_plot():
    # This component will render the gene expression plot
    return dcc.Graph(id="gene-expression-plot")
