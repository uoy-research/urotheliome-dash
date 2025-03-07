from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.fetch_data import fetch_gene_expression_data
from typing import Dict, Any, Tuple

def register_callbacks(app) -> None:
    """Register all callbacks for the application"""
    
    @app.callback(
        Output("dataset-radio", "value"),
        [
            Input("select-all-datasets", "n_clicks"),
            Input("clear-datasets", "n_clicks")
        ],
        State("dataset-radio", "options"),
        prevent_initial_call=True
    )
    def handle_dataset_controls(select_all_clicks, clear_clicks, options):
        """Handle the Select All and Clear buttons for datasets"""
        ctx = callback_context
        if not ctx.triggered:
            return no_update
            
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "select-all-datasets":
            return [option["value"] for option in options]
        elif button_id == "clear-datasets":
            return []
        return no_update
    
    @app.callback(
        output=[
            Output("gene-expression-plot", "figure"),
            Output("loading-indicator", "children"),
            Output("error-message", "children")
        ],
        inputs=[
            Input("gene-dropdown", "value"),
            Input("dataset-radio", "value"),
            Input("xaxis-dropdown", "value"),
            Input("plot-type-radio", "value")
        ],
        state=[
            State("gene-expression-plot", "figure")
        ],
        prevent_initial_call=True,
    )
    def update_plot(selected_genes: list, selected_datasets: list, x_axis: str, plot_type: str, 
                   current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str, str]:
        """Update the plot based on selected genes and datasets"""
        # Handle missing selections with specific error messages
        if not selected_genes and not selected_datasets:
            return {}, "", "Please select at least one gene and one dataset"
        if not selected_genes:
            return {}, "", "Please select at least one gene"
        if not selected_datasets:
            return {}, "", "Please select at least one dataset"
            
        try:
            # Fetch data (will use LRU cache if available)
            data = fetch_gene_expression_data(tuple(selected_genes), tuple(selected_datasets))
            
            if data.empty:
                return current_figure or {}, "", "No data available for the selected combination"
                
            # Create plot with dynamic x-axis and plot type
            if plot_type == "violin+points":
                # TODO - not coloured by dataset, no hover_data
                #plot_data = go.Violin(x=data[x_axis], y=data["TPM"], points='all', pointpos=0)
                #fig = go.Figure(plot_data)
                
                #UNCOMMENT TO SHOW POINTS NEXT TO VIOLIN PLOT + HOVER DATA, YOU WILL HAVE TO COMMENT OUT 2 LINES ABOVE.
                fig = px.violin(data, x=x_axis, y='TPM', color="DatasetName", points="all",
                              hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                        'SubstrateType', 'Gender', 'Stage', 'Status',
                                        'NhuDifferentiation'])
            elif plot_type == "violin":
                fig = px.violin(data, x=x_axis, y='TPM', color="DatasetName",
                              hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                        'SubstrateType', 'Gender', 'Stage', 'Status',
                                        'NhuDifferentiation'])
            elif plot_type == "box+points":
                fig = px.box(data, x=x_axis, y='TPM', color="DatasetName", points="all",
                           hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                     'SubstrateType', 'Gender', 'Stage', 'Status',
                                     'NhuDifferentiation'])
            elif plot_type == "box":
                fig = px.box(data, x=x_axis, y='TPM', color="DatasetName",
                           hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                     'SubstrateType', 'Gender', 'Stage', 'Status',
                                     'NhuDifferentiation'])
            else:  # strip/swarm plot
                fig = px.strip(data, x=x_axis, y='TPM', color="DatasetName",
                             hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                       'SubstrateType', 'Gender', 'Stage', 'Status',
                                       'NhuDifferentiation'])
            
            # Update layout with dynamic x-axis title
            x_axis_titles = {
                "GeneName": "Gene Name",
                "NhuDifferentiation": "NHU",
                "TissueName": "Tissue",
                "Gender": "Gender",
                "SubstrateType": "Substrate",
                "SubsetName": "Dataset Subset",
                "Stage": "Tumor Stage",
                "Status": "Vital Status"
            }
            
            # Set tick angle based on number of unique values
            tick_angle = 90 if len(data[x_axis].unique()) > 10 else 0
            
            fig.update_layout(
                title="Gene Expression Data",
                title_x=0.5,
                xaxis_title=x_axis_titles.get(x_axis, x_axis),
                yaxis_title="TPM (Transcripts Per Million)",
                showlegend=True,
                legend_title="Dataset",
                xaxis={'automargin': True, 'tickangle': tick_angle},
                margin={'t': 50, 'l': 50, 'r': 50, 'b': 100}
            )
            
            fig.update_traces(
                marker=dict(size=6, opacity=0.7),
                jitter=0.35
            )
            
            return fig, "", ""  # Empty error message on success
            
        except Exception as e:
            print(f"Error updating plot: {str(e)}")
            return current_figure or {}, "", f"Error: {str(e)}"
