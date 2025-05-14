import dash
from callbacks.gene_callbacks import register_callbacks
from layouts.layout_manager import create_layout, register_layout_callbacks
from layouts.navigation import register_navbar_callbacks
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dotenv import load_dotenv

load_dotenv()

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME  # Add Font Awesome for icons
    ],
    suppress_callback_exceptions=True,
    use_pages=False  # We're using our own routing solution
)

# Set the main layout with the layout manager
app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "light",
    },
    children=create_layout()
)
app.title = "Urotheliome"

# Register all callbacks
register_layout_callbacks(app)  # For page routing
register_navbar_callbacks(app)  # For navbar toggle on mobile
register_callbacks(app)         # For gene visualization

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
