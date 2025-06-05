from dash import html
import dash_bootstrap_components as dbc

def home_layout() -> html.Div:
    """
    Create the home page layout with mission statement, logos, and usage guide
    Returns:
        Dash HTML Div containing the home page layout
    """
    # Container style for consistent look
    container_style = {"max-width": "1200px"}
    
    # Mission statement section
    mission_section = dbc.Card(
        dbc.CardBody([
            html.H3("About", className="card-title text-primary"),
            html.P(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
                "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
                "commodo consequat. Duis aute irure dolor in reprehenderit in"
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
                "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
                "commodo consequat. Duis aute irure dolor in reprehenderit in",
                className="card-text"
            ),
        ]),
        className="mb-4 shadow-sm"
    )
    
    # Usage guide section
    guide_section = dbc.Card(
        dbc.CardBody([
            html.H3("How to Use", className="card-title text-primary"),
            html.P("Follow these steps to get started with exploring Urotheliome data:"),
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.Strong("1. Navigate to the Gene Explorer: "),
                    "Click on 'Gene Explorer' in the navigation bar to access the interactive visualization tools."
                ]),
                dbc.ListGroupItem([
                    html.Strong("2. Select genes of interest: "),
                    "Use the searchable dropdown menu to select the gene(s) you wish to analyze."
                ]),
                dbc.ListGroupItem([
                    html.Strong("3. Choose visualization options: "),
                    "Select the desired plot type (scatter, violin, or box) and axis variables."
                ]),
                dbc.ListGroupItem([
                    html.Strong("4. Compare specific genes: "),
                    "Use the Gene Comparison tab to directly compare expression patterns between two selected genes."
                ]),
            ]),
        ]),
        className="mb-4 shadow-sm"
    )
    
    # Logo section - now positioned at the bottom with alternating heights
    partners_heading = html.H3("Supported by", className="text-primary text-center mt-5 mb-5")
    
    # Top row with 2 logos (taller)
    logo_row_top = dbc.Row([
        dbc.Col(html.Img(src="/assets/Logos/york-biology-logo.jpg", className="img-fluid", style={"height": "120px"}, alt="University of York Biology Department logo"), 
                width="auto", className="text-center mx-5 px-4"),
        dbc.Col(html.Img(src="/assets/Logos/ukri-bbsrc-square-logo.png", className="img-fluid", style={"height": "120px"}, alt="UKRI BBSRC funding logo"), 
                width="auto", className="text-center mx-5 px-4"),
    ], justify="center", align="center", className="mb-4")
    
    # Bottom row with 3 logos (shorter)
    logo_row_bottom = dbc.Row([
        dbc.Col(html.Img(src="/assets/Logos/ybri-white-logo.png", className="img-fluid", style={"height": "90px", "background-color": "gray", "padding": "10px"}, alt="York Biomedical Research Institute logo"), 
                width="auto", className="text-center mx-5"),
        dbc.Col(html.Img(src="/assets/Logos/YAC-logo-long.png", className="img-fluid", style={"height": "90px", "padding": "10px"}, alt="York Against Cancer logo"), 
                width="auto", className="text-center mx-5"),
        dbc.Col(html.Img(src="/assets/Logos/Astellas-logo.svg", className="img-fluid", style={"height": "90px", "padding": "10px"}, alt="Astellas Pharma logo"), 
                width="auto", className="text-center mx-5"),
    ], justify="center", align="center", className="mb-5")
    
    return html.Div([
        dbc.Container([
            html.H1("Welcome to the Urotheliome Project", 
                   className="text-center my-4 text-primary"),
            
            dbc.Row([
                dbc.Col([mission_section], md=12)
            ]),
            
            dbc.Row([
                dbc.Col([guide_section], md=12)
            ]),
            
            partners_heading,
            logo_row_top,
            logo_row_bottom
        ], style=container_style),
    ]) 