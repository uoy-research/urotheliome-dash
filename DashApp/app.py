import dash
from callbacks.gene_callbacks import register_callbacks
from layouts.gene_dashboard_layout import gene_dashboard_layout
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dotenv import load_dotenv

load_dotenv()

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Main Layout
app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "light",
    },
    children=gene_dashboard_layout()
)
app.title = "Urotheliome"

# Register callbacks (to update the UI based on user interaction)
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
