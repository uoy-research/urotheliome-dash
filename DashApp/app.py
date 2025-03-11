import dash
from callbacks.gene_callbacks import register_callbacks
from layouts.gene_dashboard_layout import gene_dashboard_layout

# Initialize Dash app
app = dash.Dash(__name__)

# Main Layout
app.layout = gene_dashboard_layout()

# Register callbacks (to update the UI based on user interaction)
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
