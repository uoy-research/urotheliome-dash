from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

def create_navbar():
    """
    Create a navigation bar with Home and Gene Explorer links
    Returns:
        Dash Bootstrap Navbar component
    """
    container_style = {"max-width": "1200px"}
    
    # CSS-based logo placeholder for the navbar
    navbar_logo = html.Div([
        html.Span("U", className="placeholder-logo-text")
    ], className="placeholder-logo me-2", style={"width": "30px", "height": "30px", "padding": "0", "line-height": "30px"})
    
    return dbc.Navbar(
        dbc.Container(
            [
                # Brand/logo
                dbc.NavbarBrand(
                    [
                        navbar_logo,
                        "Urotheliome"
                    ],
                    href="/",
                    className="text-primary fw-bold"
                ),
                
                # Toggle button for mobile
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                
                # Navigation links with active prop set to "exact" for proper highlighting
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                            dbc.NavItem(dbc.NavLink("Gene Explorer", href="/gene-explorer", active="exact")),
                            dbc.NavItem(dbc.NavLink("Genome Browser", href="/genome-browser", active="exact"))
                        ],
                        className="ms-auto",
                        navbar=True
                    ),
                    id="navbar-collapse",
                    navbar=True,
                    is_open=False,
                ),
            ],
            fluid=True,
            style=container_style,
        ),
        color="light",
        className="shadow-sm mb-3",
        dark=False,
    )

# Add a callback to toggle the navbar when in mobile view - from Docs, will need to test
def register_navbar_callbacks(app):
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open 