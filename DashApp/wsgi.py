import webbrowser
import dash
from dash import dcc, html

from layouts import gene_dashboard_layout as gd
from app import app

server = app.server

prerendered_gene_dashboard = gd.gene_dashboard_layout()

index_page = html.Div([
    html.H1("Welcome to JBU's Data visualisation!"),
    html.H2("Below are the options available."),
    dcc.Link('Gene Viz', href='/gene-vis'),
    html.Br(),
    dcc.Link('Differential Expression', href='/gene-diff'),
    html.Br(),
    dcc.Link('Manifold', href='/manyfold'),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/gene-vis':
        return prerendered_gene_dashboard
    if pathname == '/gene-diff':
        return prerendered_gene_dashboard
    if pathname == '/manyfold':
        return prerendered_gene_dashboard
    else:
        return index_page

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/gene-diff')
    
if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8050, debug=True)

