from dash import html, dcc
import dash_bootstrap_components as dbc
from components.dropdowns import gene_dropdown, xaxis_dropdown, gene_comparison_dropdown_1, gene_comparison_dropdown_2
from components.radio_buttons import dataset_radio
from components.plots import gene_expression_plot, gene_comparison_plot

def create_control_section(title, controls):
    """Helper to create consistent control cards"""
    return dbc.Card([
        #dbc.CardHeader(title, className="p-2"),
        dbc.CardBody(controls, className="p-2")
    ], className="mb-3")

def create_plot_section(plot_component):
    """Helper to create consistent plot cards with spinner"""
    return dbc.Spinner(
        children=dbc.Card([
            dbc.CardBody([plot_component], className="p-2")
        ]),
        color="primary",
        type="grow",
        fullscreen=False,
    )

def create_error_card(tab_id):
    """Helper to create consistent error message cards"""
    return dbc.Collapse(
        dbc.Card([
            dbc.CardBody(
                html.Div(id=f"error-alert-{tab_id}", className="text-danger"),
                className="p-2"
            )
        ], className="mb-3 border-danger"),
        id=f"error-alert-collapse-{tab_id}",
        is_open=False,
    )

def gene_dashboard_layout() -> html.Div:
    """
    Create the main dashboard layout using Bootstrap components
    Returns:
        Dash HTML Div containing the complete dashboard layout
    """
    # Common styles
    container_style = {"max-width": "1200px"}
    
    # Visualization controls
    viz_controls = [
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
    ]
    
    # Comparison controls
    comp_controls = [
        html.Label("Select First Gene", htmlFor="gene-comparison-dropdown-1", className="fw-bold small"),
        gene_comparison_dropdown_1(),
        html.Hr(className="my-2"),
        
        html.Label("Select Second Gene", htmlFor="gene-comparison-dropdown-2", className="fw-bold small mt-2"),
        gene_comparison_dropdown_2()
    ]

    # TER slider control for global controls
    ter_control = [
        html.Label("Transepithelial Electrical Resistance barrier (TER) threshold", 
                  htmlFor="ter-input", className="fw-bold"),
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Input(
                        id="ter-input",
                        type="number",
                        min=0,
                        step=0.01,
                        value=0,
                        placeholder="Enter TER threshold",
                        className="mb-2"
                    )
                ], width=10),
                dbc.Col([
                    html.Div(id="ter-value-display", className="small text-muted text-center")
                ], width=2)
            ]),
            html.Small("Only show samples with TER values above this threshold", className="text-muted")
        ], className="mt-2 mb-3")
    ]

    # Dataset control for global controls
    dataset_control = [
        html.Label("Select Datasets", htmlFor="dataset-radio", className="fw-bold"),
        dataset_radio(),
        dcc.Link("Dataset Information", href="https://docs.google.com/document/d/1yJYfFn6kdUS2KAp1tuGDLEzuR2hsscdESQTpLCxH1wU", target="_blank", className="small text-muted")
    ]

    return html.Div([
        # Main Content using a vertical layout
        dbc.Container([
            # Hidden div for loading indicator
            html.Div(id="loading-indicator", style={"display": "none"}),
            
            # For backward compatibility with callbacks (these will be hidden)
            # html.Div(id="error-alert", style={"display": "none"}),
            # dbc.Collapse(id="error-alert-collapse", is_open=False, style={"display": "none"}),
            
            # Tabs with integrated controls to the left of the plot
            dbc.Tabs(
                id="tabs",
                active_tab="gene-visualization",
                className="mb-0",
                persistence=True,
                persistence_type="memory",
                children=[
                    # Visualization Tab
                    dbc.Tab(
                        label="Gene Visualization",
                        tab_id="gene-visualization",
                        labelClassName="fw-bold",
                        id="gene-visualization-tab",
                        key="gene-visualization",
                        children=[
                            # Row containing controls on left, plot on right
                            dbc.Row([
                                # Left side - Visualization Controls (compact)
                                dbc.Col([
                                    create_control_section("Visualization Controls", viz_controls),
                                    create_error_card("viz")
                                ], md=3, className="pe-0"),
                                
                                # Right side - Graph
                                dbc.Col([
                                    create_plot_section(gene_expression_plot())
                                ], md=9, className="ps-2")
                            ])
                        ]
                    ),
                    
                    # Comparison Tab
                    dbc.Tab(
                        label="Gene Comparison",
                        tab_id="gene-comparison",
                        labelClassName="fw-bold",
                        id="gene-comparison-tab",
                        key="gene-comparison",
                        children=[
                            # Row containing controls on left, plot on right
                            dbc.Row([
                                # Left side - Comparison Controls (compact)
                                dbc.Col([
                                    create_control_section("Comparison Controls", comp_controls),
                                    create_error_card("comp")
                                ], md=3, className="pe-0"),
                                
                                # Right side - Graph
                                dbc.Col([
                                    create_plot_section(gene_comparison_plot())
                                ], md=9, className="ps-2")
                            ])
                        ]
                    ),
                ],
            ),
            
            # Global controls at the bottom
            create_control_section(
                "Global Controls",
                [
                    # TER Slider
                    *ter_control,
                    html.Hr(),
                    # Dataset selection
                    *dataset_control
                ]
            )
        ], style=container_style),
    ])
