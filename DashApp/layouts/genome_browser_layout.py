from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_bio as dashbio
from dash.dependencies import Input, Output

def genome_browser_layout() -> html.Div:
    """
    Create a genome browser layout using IGV component from dash-bio
    Returns:
        Dash HTML Div containing the genome browser layout
    """
    # Common styles
    container_style = {"max-width": "1200px"}
    
    # Define a list of genomes available in IGV
    HOSTED_GENOME_DICT = [
        {'value': 'hg38', 'label': 'Human (GRCh38/hg38)'},
        {'value': 'hg19', 'label': 'Human (GRCh37/hg19)'},
        {'value': 'mm10', 'label': 'Mouse (GRCm38/mm10)'},
        {'value': 'mm9', 'label': 'Mouse (NCBI37/mm9)'},
        {'value': 'rn6', 'label': 'Rat (RGCS 6.0/rn6)'},
        {'value': 'gorGor4', 'label': 'Gorilla (gorGor4.1/gorGor4)'},
        {'value': 'panTro4', 'label': 'Chimp (SAC 2.1.4/panTro4)'},
        {'value': 'panPan2', 'label': 'Bonobo (MPI-EVA panpan1.1/panPan2)'},
        {'value': 'canFam3', 'label': 'Dog (Broad CanFam3.1/canFam3)'},
        {'value': 'ce11', 'label': 'C. elegans (ce11)'}
    ]
    
    return html.Div([
        dbc.Container([
            html.H3("Genome Browser", className="text-primary mb-3"),
            
            dbc.Card([
                dbc.CardBody([
                    html.P("Use the interactive genome browser below to explore genomic data. Select a genome to display.", 
                           className="lead"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Genome:", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id="genome-browser-select",
                                options=[
                                    {'value': '', 'label': 'Select a genome...'}
                                ] + HOSTED_GENOME_DICT,
                                value='',  # Default to empty/no selection
                                clearable=False,
                                className="mb-4"
                            )
                        ], md=4)
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            # Wrapper with loading spinner
                            dbc.Spinner(
                                html.Div(id="igv-container", style={"height": "800px"}),
                                color="primary",
                                type="border",
                                fullscreen=False,
                            )
                        ], md=12)
                    ])
                ])
            ], className="mb-4 shadow-sm")
        ], style=container_style)
    ])

def register_genome_browser_callbacks(app):
    """
    Register callbacks for the genome browser
    Args:
        app: Dash app instance
    """
    @app.callback(
        Output("igv-container", "children"),
        Input("genome-browser-select", "value")
    )
    def update_igv_genome(selected_genome):
        """
        Create a new IGV component instance based on selected genome
        """
        if selected_genome and selected_genome != '':
            # Create the IGV component with appropriate settings
            return dashbio.Igv(
                id=f"igv-genome-{selected_genome}",  # Unique ID based on genome
                genome=selected_genome,
                minimumBases=5
            )
        # Show a placeholder when no genome is selected
        return html.Div([
            html.Div([
                html.I(className="fas fa-dna fa-3x text-muted mb-3"),
                html.H5("Genome Browser", className="mb-3"),
                html.P("Please select a genome from the dropdown above to load the browser", 
                       className="text-muted"),
            ], className="text-center"),
        ], className="d-flex align-items-center justify-content-center h-100 border border-light") 