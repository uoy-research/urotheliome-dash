from dash import html
import dash_bootstrap_components as dbc

def create_footer():
    """
    Create a consistent footer for all pages
    Returns:
        Dash Bootstrap Container component
    """
    container_style = {"max-width": "1200px"}
    
    return html.Footer(
            dbc.Container([
                html.Hr(),
                dbc.Row([
                    dbc.Col(
                        html.P([
                            html.A("University of York Legal Statements", 
                                  href="https://www.york.ac.uk/about/legal-statements/", 
                                  target="_blank",
                                  className="text-muted"),
                            " | ",
                            html.A("Accessibility", 
                                  href="/accessibility", 
                                  className="text-muted")
                        ], className="small")
                    ),
                    dbc.Col([
                        html.P([
                            "© ", html.Time("2025"), " University of York"
                        ], className="text-muted small text-end")
                    ], width=3)
                ])
            ], fluid=True, className="py-2", style=container_style),  # Apply max-width constraint
            className="bg-light mt-auto py-2"
        )