from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
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

def ter_radio():

    return html.Div([
        # TER radio buttons
        dbc.RadioItems(
            options=[
                {"label": "All values", "value": 0},
                {"label": "tight barrier >= 500Ω.cm^2", "value": 500},
                {"label": "tight barrier >= 1000Ω.cm^2", "value": 1000},
            ],
            value=0,
            id="ter-input",
        ),
    ])

def y_axis_radio():

    return html.Div([
        # y-axis radio buttons
        dbc.RadioItems(
            options=[
                {"label": "Linear", "value": "linear"},
                #{"label": "Log2", "value": "log2"},
                {"label": "Log10", "value": "log10"},
            ],
            value="linear",
            inline=True,
            id="y-axis-radio",
            className="mb-2 small"
        ),
    ])