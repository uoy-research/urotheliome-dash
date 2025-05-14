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
            html.H3("Mission Statement", className="card-title text-primary"),
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
    
    # Logo section with placeholders for 5 logos (using CSS instead of images)
    logo_section = dbc.Card(
        dbc.CardBody([
            # html.H3("Our Partners", className="card-title text-primary mb-4"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span("Partner Logo", className="placeholder-logo-text")
                    ], className="placeholder-logo m-2"),
                ], width={"size": 2}, className="text-center") for _ in range(5)
            ], justify="around", align="center"),
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
                    "Use the searchable dropdown menu to select the genes you wish to analyze."
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
    
    return html.Div([
        dbc.Container([
            html.H1("Welcome to the Urotheliome Project", 
                   className="text-center my-4 text-primary"),
            
            dbc.Row([
                dbc.Col([mission_section], md=12)
            ]),
            
            dbc.Row([
                dbc.Col([logo_section], md=12)
            ]),
            
            dbc.Row([
                dbc.Col([guide_section], md=12)
            ]),
        ], style=container_style),
    ]) 