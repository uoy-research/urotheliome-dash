from dash import dcc, html
import dash_bootstrap_components as dbc
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
            className="dataset-radio-group mb-3"
        ),
        
        # Select All and Clear buttons
        dbc.ButtonGroup([
            dbc.Button(
                "Select All Datasets",
                id="select-all-datasets",
                n_clicks=0,
                color="primary",
                outline=True,
                size="sm",
                className="me-2"
            ),
            dbc.Button(
                "Clear Selection",
                id="clear-datasets",
                n_clicks=0,
                color="secondary",
                outline=True,
                size="sm"
            )
        ], className="mb-3")
    ])
