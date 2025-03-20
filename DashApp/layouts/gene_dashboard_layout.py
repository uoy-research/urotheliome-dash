from dash import html, dcc
import dash_bootstrap_components as dbc
from components.dropdowns import gene_dropdown, xaxis_dropdown, gene_comparison_dropdown_1, gene_comparison_dropdown_2
from components.radio_buttons import dataset_radio
from components.plots import gene_expression_plot, gene_comparison_plot

def gene_dashboard_layout() -> html.Div:
    """
    Create the main dashboard layout using Bootstrap components
    Returns:
        Dash HTML Div containing the complete dashboard layout
    """
    return html.Div([
        # NavBar
        dbc.Navbar(
            dbc.Container(
                dbc.Row([
                    dbc.Col(
                        html.H3("Gene Expression Dashboard", className="text-primary mb-0"),
                        width="auto",
                    ),
                ]),
                fluid=True,
                style={"max-width": "1200px"},  # Apply max-width constraint
            ),
            color="light",
            className="shadow-sm mb-3",
        ),
        
        # Main Content using a vertical layout
        dbc.Container([
            # Fixed position error alert (won't push content down)
            dbc.Alert(
                id="error-alert",
                className="mb-2",
                color="danger",
                is_open=False,
                dismissable=True,
                style={"position": "fixed", "top": "70px", "right": "15px", 
                       "width": "400px", "z-index": "1000", "opacity": "0.95"}
            ),
            
            # Hidden divs to store error states and loading indicator
            dcc.Store(id="viz-error-state", data=""),
            dcc.Store(id="comp-error-state", data=""),
            html.Div(id="loading-indicator", style={"display": "none"}),
            
            # Tabs with integrated controls to the left of the plot
            dbc.Tabs(
                id="tabs",
                active_tab="gene-visualization",
                className="mb-3",
                children=[
                    # Visualization Tab
                    dbc.Tab(
                        label="Gene Visualization",
                        tab_id="gene-visualization",
                        labelClassName="fw-bold",
                        children=[
                            # Row containing controls on left, plot on right
                            dbc.Row([
                                # Left side - Visualization Controls (compact)
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Visualization Controls", className="p-2"),
                                        dbc.CardBody([
                                            html.Label("Select Genes", htmlFor="gene-dropdown", className="fw-bold small"),
                                            gene_dropdown(),
                                            html.Hr(className="my-2"),
                                            
                                            html.Label("Select X-axis", htmlFor="xaxis-dropdown", className="fw-bold small mt-2"),
                                            xaxis_dropdown(),
                                            html.Hr(className="my-2"),
                                            
                                            html.Label("Plot Type", className="fw-bold small mt-2"),
                                            dbc.RadioItems(
                                                id="plot-type-radio",
                                                options=[
                                                    {"label": "Scatter", "value": "strip"},
                                                    {"label": "Violin", "value": "violin"},
                                                    {"label": "Box", "value": "box"}
                                                ],
                                                value="strip",
                                                inline=True,
                                                className="mb-2 small"
                                            )
                                        ], className="p-2")
                                    ], className="mb-3")
                                ], md=3, className="pe-0"),
                                
                                # Right side - Graph
                                dbc.Col([
                                    dbc.Spinner(
                                        children=dbc.Card([
                                            dbc.CardBody([
                                                gene_expression_plot()
                                            ], className="p-2")
                                        ]),
                                        color="primary",
                                        type="border",
                                        fullscreen=False,
                                    )
                                ], md=9, className="ps-2")
                            ])
                        ]
                    ),
                    
                    # Comparison Tab
                    dbc.Tab(
                        label="Gene Comparison",
                        tab_id="gene-comparison",
                        labelClassName="fw-bold",
                        children=[
                            # Row containing controls on left, plot on right
                            dbc.Row([
                                # Left side - Comparison Controls (compact)
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader("Comparison Controls", className="p-2"),
                                        dbc.CardBody([
                                            html.Label("Select First Gene", htmlFor="gene-comparison-dropdown-1", className="fw-bold small"),
                                            gene_comparison_dropdown_1(),
                                            html.Hr(className="my-2"),
                                            
                                            html.Label("Select Second Gene", htmlFor="gene-comparison-dropdown-2", className="fw-bold small mt-2"),
                                            gene_comparison_dropdown_2()
                                        ], className="p-2")
                                    ], className="mb-3")
                                ], md=3, className="pe-0"),
                                
                                # Right side - Graph
                                dbc.Col([
                                    dbc.Spinner(
                                        children=dbc.Card([
                                            dbc.CardBody([
                                                gene_comparison_plot()
                                            ], className="p-2")
                                        ]),
                                        color="primary",
                                        type="border",
                                        fullscreen=False,
                                    )
                                ], md=9, className="ps-2")
                            ])
                        ]
                    ),
                ],
            ),
            
            # Global controls at the bottom
            dbc.Card([
                dbc.CardHeader("Global Controls"),
                dbc.CardBody([
                    html.Label("Select Datasets", htmlFor="dataset-radio", className="fw-bold"),
                    dataset_radio()
                    # The dataset_radio component already includes Select All and Clear buttons
                ])
            ], className="mb-3")
        ], fluid=True, className="mb-4", style={"max-width": "1200px"}),  # Apply max-width constraint
        
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
            ], fluid=True, className="py-2", style={"max-width": "1200px"}),  # Apply max-width constraint
            className="bg-light mt-auto py-2"
        )
    ])
