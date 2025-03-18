from dash import html, dcc
import dash_bootstrap_components as dbc
from components.dropdowns import gene_dropdown, xaxis_dropdown, gene_comparison_dropdown_1, gene_comparison_dropdown_2
from components.radio_buttons import dataset_radio, plot_type_radio
from components.plots import gene_expression_plot, gene_comparison_plot

def gene_dashboard_layout() -> html.Div:
    """
    Create the main dashboard layout using Bootstrap components
    Returns:
        Dash HTML Div containing the complete dashboard layout
    """
    return html.Div([
        # NavBar
        dbc.Container(
            dbc.Row(
                dbc.Col(
                    html.H2("Gene Expression Dashboard", className="my-3 text-primary"),
                    width={"size": 12},
                ),
                className="bg-light py-2 mb-4 shadow-sm"
            ),
            fluid=True,
        ),
        
        # Main Content
        dbc.Container([
            # Global Controls Section
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Global Controls", className="card-title"),
                            html.Hr(className="my-2"),
                            html.Label("Select Datasets", htmlFor="dataset-radio", className="mb-2 fw-bold"),
                            dataset_radio()
                        ])
                    ])
                ]),
                className="mb-4"
            ),
            
            # Global error alert container - now using a single alert
            html.Div(
                id="error-container",
                className="mb-3",
                children=[
                    # Single error alert for all error messages
                    dbc.Alert(
                        id="error-alert",
                        className="mb-2",
                        color="danger",
                        is_open=False,
                    ),
                    # Hidden divs to store error states for each tab
                    dcc.Store(id="viz-error-state", data=""),
                    dcc.Store(id="comp-error-state", data="")
                ]
            ),
            
            # Hidden loading indicator div - target for callbacks
            html.Div(id="loading-indicator", style={"display": "none"}),
            
            # Tabs for switching between visualization modes using Bootstrap tabs
            dbc.Tabs(
                id="tabs",
                active_tab="gene-visualization",
                children=[
                    dbc.Tab(
                        label="Gene Visualization",
                        tab_id="gene-visualization",
                        children=[
                            # Gene Visualization Tab Content
                            dbc.Card(
                                dbc.CardBody([
                                    # Controls section
                                    html.Div([
                                        html.H5("Gene Visualization Controls", className="card-title"),
                                        html.Hr(className="my-2"),
                                        dbc.Row([
                                            # Gene dropdown section
                                            dbc.Col([
                                                html.Label("Select Genes", htmlFor="gene-dropdown", className="mb-2 fw-bold"),
                                                gene_dropdown()
                                            ], md=6, className="mb-3"),
                                    
                                            # X-axis dropdown section
                                            dbc.Col([
                                                html.Label("Select X-axis", htmlFor="xaxis-dropdown", className="mb-2 fw-bold"),
                                                xaxis_dropdown()
                                            ], md=6, className="mb-3"),
                                        ]),
                                        
                                        # Plot type radio section - simplified options
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Plot Type", className="mb-2 fw-bold"),
                                                dbc.RadioItems(
                                                    id="plot-type-radio",
                                                    options=[
                                                        {"label": "Scatter", "value": "strip"},
                                                        {"label": "Violin", "value": "violin"},
                                                        {"label": "Box", "value": "box"}
                                                    ],
                                                    value="strip",
                                                    inline=True,
                                                    className="mb-3"
                                                )
                                            ], className="mb-3")
                                        ])
                                    ], className="mb-4"),
                                    
                                    # Plot section - Gene Expression Plot with spinner
                                    html.H5("Gene Expression Plot", className="mb-3"),
                                    dbc.Spinner(
                                        children=dbc.Row([
                                            dbc.Col([
                                                gene_expression_plot()
                                            ])
                                        ]),
                                        color="primary",
                                        type="border",
                                        fullscreen=False,
                                    ),
                                ]),
                            )
                        ]
                    ),
                    dbc.Tab(
                        label="Gene Comparison",
                        tab_id="gene-comparison",
                        children=[
                            # Gene Comparison Tab Content
                            dbc.Card(
                                dbc.CardBody([
                                    # Controls section
                                    html.Div([
                                        html.H5("Gene Comparison Controls", className="card-title"),
                                        html.Hr(className="my-2"),
                                        dbc.Row([
                                            # First gene dropdown
                                            dbc.Col([
                                                html.Label("Select First Gene", htmlFor="gene-comparison-dropdown-1", className="mb-2 fw-bold"),
                                                gene_comparison_dropdown_1()
                                            ], md=6, className="mb-3"),
                                            
                                            # Second gene dropdown
                                            dbc.Col([
                                                html.Label("Select Second Gene", htmlFor="gene-comparison-dropdown-2", className="mb-2 fw-bold"),
                                                gene_comparison_dropdown_2()
                                            ], md=6, className="mb-3"),
                                        ]),
                                    ], className="mb-4"),
                                    
                                    # Plot section - Gene Comparison Plot with spinner
                                    html.H5("Gene Comparison Plot", className="mb-3"),
                                    dbc.Spinner(
                                        children=dbc.Row([
                                            dbc.Col([
                                                gene_comparison_plot()
                                            ])
                                        ]),
                                        color="primary",
                                        type="border", 
                                        fullscreen=False
                                    ),
                                ]),
                            )
                        ]
                    ),
                ],
                className="mb-4",
            ),
        ], className="mb-5", style={"max-width": "1200px"}),
        
        # Footer with disclaimer
        html.Footer(
            dbc.Container([
                html.Hr(),
                dbc.Row([
                    dbc.Col(
                        html.P([
                            html.A("University of York Legal Statements", 
                                  href="https://www.york.ac.uk/about/legal-statements/", 
                                  target="_blank",
                                  className="text-muted")
                        ], className="small")
                    ),
                    dbc.Col([
                        html.P([
                            "© ", html.Time("2025"), " University of York"
                        ], className="text-muted small text-end")
                    ], width=3)
                ])
            ], className="py-3", style={"max-width": "1200px"}),
            className="bg-light mt-auto py-3"
        )
    ])
