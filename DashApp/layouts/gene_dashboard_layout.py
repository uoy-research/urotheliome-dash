from dash import html, dcc
from components.dropdowns import gene_dropdown, xaxis_dropdown
from components.radio_buttons import dataset_radio, plot_type_radio
from components.plots import gene_expression_plot

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
        
        # Controls section
        html.Div([
            # Dropdowns container
            html.Div([
                # Left container
                html.Div([
                    # Gene dropdown section
                    html.Div([
                        html.Label(
                            "Select Genes",
                            htmlFor="gene-dropdown",
                            className="dropdown-label"
                        ),
                        gene_dropdown()
                    ], className="dropdown-section"),

                    # X-axis dropdown section
                    html.Div([
                        html.Label(
                            "Select X-axis",
                            htmlFor="xaxis-dropdown",
                            className="dropdown-label"
                        ),
                        xaxis_dropdown()
                    ], className="dropdown-section"),

                    # Plot type radio section
                    html.Div([
                        plot_type_radio()
                    ], className="dropdown-section"),
                ], className="left-container"),
                # Dataset radio section
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
            
            # Error/Info messages
            html.Div(
                id="error-message",
                className="error-message"
            )
        ], className="status-container"),
        
        # Plot section
        html.Div([
            gene_expression_plot()
        ], className="plot-container")
    ])
