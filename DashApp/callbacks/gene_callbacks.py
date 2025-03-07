from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.fetch_data import fetch_gene_expression_data
from typing import Dict, Any, Tuple, List
import numpy as np
from scipy import stats
import pandas as pd

def register_callbacks(app) -> None:
    """Register all callbacks for the application"""
    
    @app.callback(
        [
            Output("gene-dropdown-container", "style"),
            Output("xaxis-dropdown-container", "style"),
            Output("plot-type-container", "style"),
            Output("gene1-dropdown-container", "style"),
            Output("gene2-dropdown-container", "style"),
            Output("gene-expression-plot-container", "style"),
            Output("gene-comparison-plot-container", "style"),
        ],
        Input("tabs", "value")
    )
    def toggle_visualization_mode(selected_tab: str) -> List[Dict[str, Any]]:
        """Toggle visibility of UI components based on the selected tab"""
        if selected_tab == "gene-visualization":
            # Show Gene Visualization, hide Gene Comparison
            return (
                {"display": "block"},  # gene-dropdown-container
                {"display": "block"},  # xaxis-dropdown-container
                {"display": "block"},  # plot-type-container
                {"display": "none"},   # gene1-dropdown-container
                {"display": "none"},   # gene2-dropdown-container
                {"display": "block"},  # gene-expression-plot-container
                {"display": "none"}    # gene-comparison-plot-container
            )
        else:  # "gene-comparison"
            # Hide Gene Visualization, show Gene Comparison
            return (
                {"display": "none"},   # gene-dropdown-container
                {"display": "none"},   # xaxis-dropdown-container
                {"display": "none"},   # plot-type-container
                {"display": "block"},  # gene1-dropdown-container
                {"display": "block"},  # gene2-dropdown-container
                {"display": "none"},   # gene-expression-plot-container
                {"display": "block"}   # gene-comparison-plot-container
            )
    
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
            Input("plot-type-radio", "value"),
            Input("tabs", "value")  # Added tab as an input to conditionally trigger
        ],
        state=[
            State("gene-expression-plot", "figure")
        ],
        prevent_initial_call=True,
    )
    def update_plot(selected_genes: list, selected_datasets: list, x_axis: str, plot_type: str, 
                   active_tab: str, current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str, str]:
        """Update the plot based on selected genes and datasets"""
        # Only update when on the gene-visualization tab
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update
            
        # Skip update if not on the gene visualization tab, unless tab change triggered the callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if active_tab != "gene-visualization" and trigger != "tabs":
            return no_update, no_update, no_update
        
        # If tab change to gene-comparison triggered this callback, don't update
        if trigger == "tabs" and active_tab == "gene-comparison":
            return no_update, no_update, no_update
        
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
                                        'NhuDifferentiation', 'SampleId'])
            elif plot_type == "violin":
                fig = px.violin(data, x=x_axis, y='TPM', color="DatasetName",
                              hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                        'SubstrateType', 'Gender', 'Stage', 'Status',
                                        'NhuDifferentiation', 'SampleId'])
            elif plot_type == "box+points":
                fig = px.box(data, x=x_axis, y='TPM', color="DatasetName", points="all",
                           hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                     'SubstrateType', 'Gender', 'Stage', 'Status',
                                     'NhuDifferentiation', 'SampleId'])
            elif plot_type == "box":
                fig = px.box(data, x=x_axis, y='TPM', color="DatasetName",
                           hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                     'SubstrateType', 'Gender', 'Stage', 'Status',
                                     'NhuDifferentiation', 'SampleId'])
            else:  # strip/swarm plot
                fig = px.strip(data, x=x_axis, y='TPM', color="DatasetName",
                             hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                                       'SubstrateType', 'Gender', 'Stage', 'Status',
                                       'NhuDifferentiation', 'SampleId'])
            
            # Update layout with dynamic x-axis title
            x_axis_titles = {
                "GeneName": "Gene Name",
                "NhuDifferentiation": "NHU",
                "TissueName": "Tissue",
                "Gender": "Gender",
                "SubstrateType": "Substrate",
                "SubsetName": "Dataset Subset",
                "Stage": "Tumor Stage",
                "Status": "Vital Status",
                "SampleId": "Sample ID"
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
            
    @app.callback(
        output=[
            Output("gene-comparison-plot", "figure"),
            Output("error-message", "children", allow_duplicate=True)
        ],
        inputs=[
            Input("gene-comparison-dropdown-1", "value"),
            Input("gene-comparison-dropdown-2", "value"),
            Input("dataset-radio", "value"),
            Input("tabs", "value")  # Added tab as an input to conditionally trigger
        ],
        state=[
            State("gene-comparison-plot", "figure")
        ],
        prevent_initial_call=True,
    )
    def update_comparison_plot(gene1: str, gene2: str, selected_datasets: list, 
                              active_tab: str, current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        """Update the gene comparison scatter plot based on selected genes"""
        # Only update when on the gene-comparison tab
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update
            
        # Skip update if not on the gene comparison tab, unless tab change triggered the callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if active_tab != "gene-comparison" and trigger != "tabs":
            return no_update, no_update
        
        # If tab change to gene-visualization triggered this callback, don't update
        if trigger == "tabs" and active_tab == "gene-visualization":
            return no_update, no_update
            
        # Handle missing selections with specific error messages
        if not gene1 and not gene2:
            return current_figure or {}, "Please select two genes for comparison"
        if not gene1:
            return current_figure or {}, "Please select the first gene"
        if not gene2:
            return current_figure or {}, "Please select the second gene"
        if gene1 == gene2:
            return current_figure or {}, "Please select different genes for comparison"
        if not selected_datasets:
            return current_figure or {}, "Please select at least one dataset"
            
        try:
            # Fetch data for both genes
            selected_genes = (gene1, gene2)
            data = fetch_gene_expression_data(selected_genes, tuple(selected_datasets))
            
            if data.empty:
                return current_figure or {}, "No data available for the selected combination"
                
            # Process data for scatter plot
            # We need to pivot the data to have one row per sample with TPM values for both genes
            gene1_data = data[data['GeneName'] == gene1].copy()
            gene2_data = data[data['GeneName'] == gene2].copy()
            
            # Count data points for each gene
            gene1_count = len(gene1_data)
            gene2_count = len(gene2_data)
            
            # Define metadata columns that we want to preserve for hover data
            metadata_columns = ['DatasetName', 'SubsetName', 'TissueName', 'SubstrateType', 
                                'Gender', 'Stage', 'Status', 'NhuDifferentiation']
            available_metadata = [col for col in metadata_columns if col in data.columns]
            
            # Rename TPM columns for clarity
            gene1_data = gene1_data.rename(columns={'TPM': f'{gene1}_TPM'})
            gene2_data = gene2_data.rename(columns={'TPM': f'{gene2}_TPM'})
            
            # Check if SampleId is available
            if 'SampleId' not in gene1_data.columns:
                return current_figure or {}, "Sample ID information is not available for proper gene comparison. Please contact the administrator."
            
            # Keep only necessary columns (SampleId, TPM, and all available metadata)
            gene1_cols = ['SampleId'] + available_metadata + [f'{gene1}_TPM']
            gene2_cols = ['SampleId'] + [f'{gene2}_TPM']
            
            gene1_data = gene1_data[gene1_cols].drop_duplicates('SampleId')
            gene2_data = gene2_data[gene2_cols].drop_duplicates('SampleId')
            
            # Merge the two dataframes using only SampleId
            merged_data = gene1_data.merge(
                gene2_data,
                on='SampleId',
                how='inner'
            )
            
            # Find out how many points we matched
            matched_count = len(merged_data)
            
            # Display diagnostic message
            diag_message = f"Found {gene1_count} samples for {gene1}, {gene2_count} samples for {gene2}, and {matched_count} matching samples."
            
            # Create scatter plot
            if not merged_data.empty:
                # Define hover data to include both gene TPM values and all metadata
                hover_data = {
                    'SampleId': True,
                    f'{gene1}_TPM': True,
                    f'{gene2}_TPM': True
                }
                
                # Add all available metadata columns to hover data
                for col in available_metadata:
                    if col in merged_data.columns:
                        hover_data[col] = True
                
                fig = px.scatter(
                    merged_data, 
                    x=f'{gene1}_TPM', 
                    y=f'{gene2}_TPM', 
                    color="DatasetName" if "DatasetName" in merged_data.columns else None,
                    hover_data=hover_data,
                    opacity=0.7,
                    size_max=10
                )
                
                fig.update_layout(
                    title=f"Gene Comparison: {gene1} vs {gene2}",
                    title_x=0.5,
                    xaxis_title=f"{gene1} TPM",
                    yaxis_title=f"{gene2} TPM",
                    showlegend=True,
                    legend_title="Dataset" if "DatasetName" in merged_data.columns else None,
                    margin={'t': 50, 'l': 50, 'r': 50, 'b': 50}
                )
                
                # Find the maximum value for both axes to set the line range
                max_val = max(
                    merged_data[f'{gene1}_TPM'].max() if not merged_data.empty else 1, 
                    merged_data[f'{gene2}_TPM'].max() if not merged_data.empty else 1
                )
                
                # Add a line of identity (y=x) for reference
                fig.add_trace(
                    go.Scatter(
                        x=[0, max_val],
                        y=[0, max_val],
                        mode='lines',
                        line=dict(color='rgba(0,0,0,0.5)', dash='dash', width=2),
                        name='1:1 Line (y=x)',
                        showlegend=True
                    )
                )
                
                # Calculate linear regression
                x_values = merged_data[f'{gene1}_TPM'].values
                y_values = merged_data[f'{gene2}_TPM'].values
                
                # Only calculate regression if we have enough data points
                if len(x_values) > 1:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
                    r_squared = r_value**2
                    
                    # Create x values for the regression line
                    x_reg = np.array([0, max_val])
                    y_reg = intercept + slope * x_reg
                    
                    # Add regression line
                    fig.add_trace(
                        go.Scatter(
                            x=x_reg,
                            y=y_reg,
                            mode='lines',
                            line=dict(color='rgba(255,0,0,0.7)', width=2),
                            name=f'Regression Line (y = {slope:.2f}x + {intercept:.2f}, R² = {r_squared:.2f})',
                            showlegend=True
                        )
                    )
                
                # Update marker properties
                fig.update_traces(
                    marker=dict(
                        size=8,
                        opacity=0.7,
                        line=dict(width=1, color='DarkSlateGrey')
                    ),
                    selector=dict(mode='markers')
                )
                
                # Add an annotation with the diagnostic info
                fig.add_annotation(
                    text=diag_message,
                    xref="paper", yref="paper",
                    x=0.5, y=0,
                    showarrow=False,
                    font=dict(size=10, color="gray"),
                    bgcolor="rgba(255, 255, 255, 0.7)",
                    bordercolor="gray",
                    borderwidth=1,
                    borderpad=4,
                    align="center"
                )
                
                return fig, ""
            else:
                return current_figure or {}, f"No matching samples found for both genes in the selected datasets. {diag_message}"
                
        except Exception as e:
            print(f"Error updating comparison plot: {str(e)}")
            return current_figure or {}, f"Error: {str(e)}"
