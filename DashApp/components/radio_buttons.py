from dash import dcc, html
from data.fetch_names import fetch_datasets

def dataset_radio():
    datasets = fetch_datasets()  # Fetch dataset names from the database
    radio_options = [{"label": dataset, "value": dataset} for dataset in datasets]
    
    return html.Div([
        # Dataset checklist
        dcc.Checklist(
            id="dataset-radio",
            options=radio_options,
            value=[],  # No default value
            labelStyle={'display': 'block', 'margin-bottom': '10px'},
            className="dataset-radio-group"
        ),
        
        # Select All and Clear buttons
        html.Div([
            html.Button(
                "Select All Datasets",
                id="select-all-datasets",
                n_clicks=0,
                className="dataset-control-btn"
            ),
            html.Button(
                "Clear Selection",
                id="clear-datasets",
                n_clicks=0,
                className="dataset-control-btn"
            )
        ], className="dataset-controls")
    ])

# Plot type radio buttons
def plot_type_radio():
    return html.Div([
        html.Label("Select Plot Type", className="dropdown-label"),
        dcc.RadioItems(
            id="plot-type-radio",
            options=[
                {"label": "Scatter", "value": "strip"},
                {"label": "Violin", "value": "violin"},
                {"label": "Violin and Points", "value": "violin+points"},
                {"label": "Box", "value": "box"},
                {"label": "Box and Points", "value": "box+points"}
            ],
            value="strip",
            className="plot-type-group"
        )
    ])
