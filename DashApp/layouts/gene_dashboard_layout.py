from dash import html, dcc
from components.dropdowns import gene_dropdown, xaxis_dropdown, gene_comparison_dropdown_1, gene_comparison_dropdown_2
from components.radio_buttons import dataset_radio, plot_type_radio
from components.plots import gene_expression_plot, gene_comparison_plot

def gene_dashboard_layout() -> html.Div:
    """
    Create the main dashboard layout
    Returns:
        Dash HTML Div containing the complete dashboard layout
    """
    return html.Div([
        # Header
        html.H1("Gene Expression Visualization Dashboard", 
                style={'textAlign': 'center'}),
        
        # Tabs for switching between visualization modes
        dcc.Tabs(id="tabs", value='gene-visualization', children=[
            dcc.Tab(label='Gene Visualization', value='gene-visualization'),
            dcc.Tab(label='Gene Comparison', value='gene-comparison'),
        ], style={'marginBottom': '0px'}),
        
        # Controls section
        html.Div([
            # Dropdowns container
            html.Div([
                # Left container - Gene Visualization controls
                html.Div([
                    # Gene dropdown section
                    html.Div([
                        html.Label(
                            "Select Genes",
                            htmlFor="gene-dropdown",
                            className="dropdown-label"
                        ),
                        gene_dropdown()
                    ], className="dropdown-section", id="gene-dropdown-container"),

                    # X-axis dropdown section
                    html.Div([
                        html.Label(
                            "Select X-axis",
                            htmlFor="xaxis-dropdown",
                            className="dropdown-label"
                        ),
                        xaxis_dropdown()
                    ], className="dropdown-section", id="xaxis-dropdown-container"),

                    # Plot type radio section
                    html.Div([
                        plot_type_radio()
                    ], className="dropdown-section", id="plot-type-container"),
                    
                    # Gene Comparison controls
                    html.Div([
                        html.Label(
                            "Select First Gene",
                            htmlFor="gene-comparison-dropdown-1",
                            className="dropdown-label"
                        ),
                        gene_comparison_dropdown_1()
                    ], className="dropdown-section", id="gene1-dropdown-container", style={'display': 'none'}),
                    
                    html.Div([
                        html.Label(
                            "Select Second Gene",
                            htmlFor="gene-comparison-dropdown-2",
                            className="dropdown-label"
                        ),
                        gene_comparison_dropdown_2()
                    ], className="dropdown-section", id="gene2-dropdown-container", style={'display': 'none'}),
                    
                ], className="left-container"),
                
                # Dataset radio section (common to both views)
                html.Div([
                    html.Label(
                        "Select Datasets",
                        htmlFor="dataset-radio",
                        className="dropdown-label"
                    ),
                    dataset_radio()
                ], className="dropdown-section"),
            ], className="dropdown-container"),
        ], className="control-panel"),
        
        # Status section (Loading and Error messages)
        html.Div([
            # Loading indicator
            html.Div([
                dcc.Loading(
                    id="loading-1",
                    type="circle",
                    children=[html.Div(id="loading-indicator")],
                )
            ], className="loading-container"),
            
            # Error/Info messages (common to both views)
            html.Div(
                id="error-message",
                className="error-message"
            )
        ], className="status-container"),
        
        # Plot section - Gene Expression Plot
        html.Div([
            gene_expression_plot()
        ], className="plot-container", id="gene-expression-plot-container"),
        
        # Plot section - Gene Comparison Plot
        html.Div([
            gene_comparison_plot()
        ], className="plot-container", id="gene-comparison-plot-container", style={'display': 'none'})
    ])
