from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.fetch_data import fetch_gene_expression_data
from typing import Dict, Any, Tuple, List
import numpy as np
from scipy import stats

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
    
    # clear error messages when selections change
    @app.callback(
        [Output("error-alert", "children"),
         Output("error-alert", "is_open")],
        [Input("dataset-radio", "value"),
         Input("gene-dropdown", "value"),
         Input("gene-comparison-dropdown-1", "value"),
         Input("gene-comparison-dropdown-2", "value"),
         Input("tabs", "active_tab")],
        prevent_initial_call=True
    )
    def manage_error_messages(selected_datasets, selected_genes, gene1, gene2, active_tab):
        """Manage error messages based on selection changes and active tab"""
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update
        
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # If tab changes, show the error for the current tab (if any)
        if trigger == "tabs":
            # Since we don't have viz_error and comp_error parameters,
            # we'll just clear the error message when changing tabs
            return "", False
        
        # Clear the appropriate error based on which input triggered the callback
        if trigger == "dataset-radio":
            # Dataset changes affect both tabs, so clear all errors
            return "", False
        elif trigger == "gene-dropdown" and active_tab == "gene-visualization":
            # Clear visualization error
            return "", False
        elif trigger in ["gene-comparison-dropdown-1", "gene-comparison-dropdown-2"] and active_tab == "gene-comparison":
            # Clear comparison error
            return "", False
        
        return no_update, no_update
    
    @app.callback(
        output=[
            Output("gene-expression-plot", "figure"),
            Output("loading-indicator", "children"),
            Output("error-alert", "children", allow_duplicate=True),
            Output("error-alert", "is_open", allow_duplicate=True),
        ],
        inputs=[
            Input("gene-dropdown", "value"),
            Input("dataset-radio", "value"),
            Input("xaxis-dropdown", "value"),
            Input("plot-type-radio", "value"),
            Input("tabs", "active_tab")
        ],
        state=[
            State("gene-expression-plot", "figure")
        ],
        prevent_initial_call=True,
    )
    def update_plot(selected_genes: list, selected_datasets: list, x_axis: str, plot_type: str, 
                   active_tab: str, current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str, str, bool]:
        """Update the plot based on selected genes and datasets"""
        # Only update when on the gene-visualization tab
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update
            
        # Skip update if not on the gene visualization tab, unless tab change triggered the callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if active_tab != "gene-visualization" and trigger != "tabs":
            return no_update, no_update, no_update, no_update
        
        # If tab change to gene-comparison triggered this callback, don't update
        if trigger == "tabs" and active_tab == "gene-comparison":
            return no_update, no_update, no_update, no_update
        
        # Handle missing selections with specific error messages
        if not selected_genes and not selected_datasets:
            error_msg = "Please select at least one gene and one dataset"
            return {}, "", error_msg, True
        if not selected_genes:
            error_msg = "Please select at least one gene"
            return {}, "", error_msg, True
        if not selected_datasets:
            error_msg = "Please select at least one dataset"
            return {}, "", error_msg, True
            
        try:
            # Fetch data (will use LRU cache if available)
            data = fetch_gene_expression_data(tuple(selected_genes), tuple(selected_datasets))
            
            if data.empty:
                error_msg = "No data available for the selected combination"
                return current_figure or {}, "", error_msg, True
                
            # Create plot with dynamic x-axis and plot type
            if plot_type == "violin":
                fig = px.violin(
                    data, 
                    x=x_axis, 
                    y='TPM', 
                    color="DatasetName", 
                    points="all",  # Always show all points with violin plots
                    hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                               'SubstrateType', 'Gender', 'Stage', 'Status',
                               'NhuDifferentiation', 'SampleId']
                )
            elif plot_type == "box":
                fig = px.box(
                    data, 
                    x=x_axis, 
                    y='TPM', 
                    color="DatasetName", 
                    points="all",  # Always show all points with box plots
                    hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                               'SubstrateType', 'Gender', 'Stage', 'Status',
                               'NhuDifferentiation', 'SampleId']
                )
            else:  # strip/swarm plot (default)
                fig = px.strip(
                    data, 
                    x=x_axis, 
                    y='TPM', 
                    color="DatasetName",
                    hover_data=['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                               'SubstrateType', 'Gender', 'Stage', 'Status',
                               'NhuDifferentiation', 'SampleId']
                )
            
            # Update layout for better appearance
            fig.update_layout(
                title=f"Expression of {', '.join(selected_genes)} by {x_axis}",
                xaxis_title=x_axis,
                yaxis_title="TPM (Transcripts Per Million)",
                xaxis={'categoryorder': 'total ascending'},
                plot_bgcolor="white",
                legend_title_text="Dataset",
                height=600,  # Increased height for better visibility
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # Update grid and axis lines for better readability
            fig.update_xaxes(
                gridcolor='rgba(0,0,0,0.05)',
                gridwidth=1,
                linecolor='rgba(0,0,0,0.2)',
                linewidth=1
            )
            
            fig.update_yaxes(
                gridcolor='rgba(0,0,0,0.05)',
                gridwidth=1,
                linecolor='rgba(0,0,0,0.2)',
                linewidth=1
            )
            
            return fig, "", "", False
            
        except Exception as e:
            error_msg = f"Error generating plot: {str(e)}"
            return current_figure or {}, "", error_msg, True
    
    @app.callback(
        output=[
            Output("gene-comparison-plot", "figure"),
            Output("error-alert", "children", allow_duplicate=True),
            Output("error-alert", "is_open", allow_duplicate=True),
        ],
        inputs=[
            Input("gene-comparison-dropdown-1", "value"),
            Input("gene-comparison-dropdown-2", "value"),
            Input("dataset-radio", "value"),
            Input("tabs", "active_tab")
        ],
        state=[
            State("gene-comparison-plot", "figure")
        ],
        prevent_initial_call=True,
    )
    def update_comparison_plot(gene1: str, gene2: str, selected_datasets: list, 
                              active_tab: str, current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str, bool]:
        """Update the gene comparison scatter plot based on selected genes"""
        # Only update when on the gene-comparison tab
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update
            
        # Skip update if not on the gene comparison tab, unless tab change triggered the callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if active_tab != "gene-comparison" and trigger != "tabs":
            return no_update, no_update, no_update
        
        # If tab change to gene-visualization triggered this callback, don't update
        if trigger == "tabs" and active_tab == "gene-visualization":
            return no_update, no_update, no_update
        
        # Handle missing selections with specific error messages
        if not gene1 and not gene2:
            error_msg = "Please select two genes for comparison"
            return current_figure or {}, error_msg, True
        if not gene1:
            error_msg = "Please select the first gene"
            return current_figure or {}, error_msg, True
        if not gene2:
            error_msg = "Please select the second gene"
            return current_figure or {}, error_msg, True
        if gene1 == gene2:
            error_msg = "Please select different genes for comparison"
            return current_figure or {}, error_msg, True
        if not selected_datasets:
            error_msg = "Please select at least one dataset"
            return current_figure or {}, error_msg, True
            
        try:
            # Fetch data for both genes
            data = fetch_gene_expression_data((gene1, gene2), tuple(selected_datasets))
            
            if data.empty:
                error_msg = "No data available for the selected combination"
                return current_figure or {}, error_msg, True
                
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
                error_msg = "Sample ID information is not available for proper gene comparison. Please contact the administrator."
                return current_figure or {}, error_msg, True
            
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
                    xaxis_title=f"{gene1} Expression (TPM)",
                    yaxis_title=f"{gene2} Expression (TPM)",
                    plot_bgcolor="white",
                    legend_title_text="Dataset",
                    height=600,  # Increased height for better visibility
                    margin=dict(l=50, r=50, t=80, b=50)
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
                
                # Ordinary least squares regression using linregress
                # Only calculate regression if we have enough data points
                if len(x_values) > 1:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
                    r_squared = r_value**2
                    
                    # Create x values for the regression line
                    x_reg = np.array([0, max_val])
                    y_reg = intercept + slope * x_reg
                    
                    # Add regression line (simplified legend entry)
                    fig.add_trace(
                        go.Scatter(
                            x=x_reg,
                            y=y_reg,
                            mode='lines',
                            line=dict(color='rgba(255,0,0,0.7)', width=2),
                            name='Regression Line',
                            showlegend=True
                        )
                    )
                    
                    # Include regression equation in the title instead of as an annotation
                    regression_text = f"(y = {slope:.2f}x + {intercept:.2f}, R² = {r_squared:.2f})"
                    fig.update_layout(
                        title=f"Gene Comparison: {gene1} vs {gene2} - {regression_text}"
                    )
                else:
                    fig.update_layout(
                        title=f"Gene Comparison: {gene1} vs {gene2}"
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
                
                # Update grid and axis lines for better readability
                fig.update_xaxes(
                    gridcolor='rgba(0,0,0,0.05)',
                    gridwidth=1,
                    linecolor='rgba(0,0,0,0.2)',
                    linewidth=1
                )
                
                fig.update_yaxes(
                    gridcolor='rgba(0,0,0,0.05)',
                    gridwidth=1,
                    linecolor='rgba(0,0,0,0.2)',
                    linewidth=1
                )
                
                return fig, "", False
            else:
                error_msg = f"No matching samples found for both genes in the selected datasets. {diag_message}"
                return current_figure or {}, error_msg, True
                
        except Exception as e:
            error_msg = f"Error generating comparison plot: {str(e)}"
            return current_figure or {}, error_msg, True
