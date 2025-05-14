from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from layouts.navigation import create_navbar
from layouts.footer import create_footer
from layouts.home_layout import home_layout
from layouts.gene_dashboard_layout import gene_dashboard_layout
from layouts.genome_browser_layout import genome_browser_layout, register_genome_browser_callbacks

def create_layout():
    """
    Create the main app layout with navigation and page content
    Returns:
        Dash HTML Div containing the complete layout with navigation
    """
    # Create the layout with a URL Location component
    return html.Div([
        dbc.Container(fluid=True, children=[
            # URL Location component - to track page location
            dcc.Location(id="url", refresh=False),
            
            # Navigation bar - consistent across all pages
            create_navbar(),
            
            # Content - changes based on URL
            html.Div(id="page-content")
        ], className="px-0 d-flex flex-column min-vh-100"),
        
        # Footer - consistent across all pages
        create_footer()
    ])

def register_layout_callbacks(app):
    """
    Register callbacks to update page content based on URL
    Args:
        app: Dash app instance
    """
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def display_page(pathname):
        if pathname == "/gene-explorer" or pathname == "/gene-explorer/":
            return gene_dashboard_layout()
        elif pathname == "/genome-browser" or pathname == "/genome-browser/":
            return genome_browser_layout()
        else:
            # Default to home layout
            return home_layout()
            
    # Register genome browser callbacks
    register_genome_browser_callbacks(app) 