from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.fetch_data import fetch_gene_expression_data
from typing import Dict, Any, Tuple
import numpy as np
from scipy import stats
from dash import html
import pandas as pd

def register_callbacks(app) -> None:
    """Register all callbacks for the application"""
    
    @app.callback(
        Output("ter-value-display", "children"),
        Input("ter-input", "value")
    )
    def update_ter_display(value):
        """Update the displayed TER threshold value"""
        # Handle None value when the input is empty
        if value is None:
            value = 0
        return f"TER >= {value}"
    
    @app.callback(
        Output("dataset-radio", "value"),
        [Input("select-all-datasets", "n_clicks"), Input("clear-datasets", "n_clicks")],
        State("dataset-radio", "options"),
        prevent_initial_call=True
    )
    def handle_dataset_controls(select_all_clicks, clear_clicks, options):
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
        [Output("error-alert-viz", "children"), 
         Output("error-alert-collapse-viz", "is_open"),
         Output("error-alert-comp", "children"),
         Output("error-alert-collapse-comp", "is_open")],
        [Input("dataset-radio", "value"),
         Input("gene-dropdown", "value"),
         Input("gene-comparison-dropdown-1", "value"),
         Input("gene-comparison-dropdown-2", "value"),
         Input("tabs", "active_tab"),
         Input("ter-input", "value")],
        prevent_initial_call=True
    )
    def manage_error_messages(selected_datasets, selected_genes, gene1, gene2, active_tab, ter_threshold):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update
        
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Clear error message for tab changes or relevant input changes
        if trigger == "tabs":
            # Clear all error messages on tab change
            return "", False, "", False
        
        # Clear visualization tab errors
        if (active_tab == "gene-visualization" and 
            (trigger == "dataset-radio" or 
             trigger == "ter-input" or 
             trigger == "gene-dropdown")):
            return "", False, no_update, no_update
            
        # Clear comparison tab errors
        if (active_tab == "gene-comparison" and 
            (trigger == "dataset-radio" or 
             trigger == "ter-input" or 
             trigger in ["gene-comparison-dropdown-1", "gene-comparison-dropdown-2"])):
            return no_update, no_update, "", False
        
        return no_update, no_update, no_update, no_update
    
    def apply_common_styling(fig):
        """Apply common styling to all plots"""
        fig.update_layout(
            plot_bgcolor="white",
            height=600,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        for axis in [fig.update_xaxes, fig.update_yaxes]:
            axis(
                gridcolor='rgba(0,0,0,0.05)',
                gridwidth=1,
                linecolor='rgba(0,0,0,0.2)',
                linewidth=1,
                range=[0, None]
            )
        
        return fig
    
    @app.callback(
        output=[
            Output("gene-expression-plot", "figure"),
            Output("loading-indicator", "children"),
            Output("error-alert-viz", "children", allow_duplicate=True),
            Output("error-alert-collapse-viz", "is_open", allow_duplicate=True),
        ],
        inputs=[
            Input("gene-dropdown", "value"),
            Input("dataset-radio", "value"),
            Input("xaxis-dropdown", "value"),
            Input("plot-type-radio", "value"),
            Input("tabs", "active_tab"),
            Input("ter-input", "value")
        ],
        state=[State("gene-expression-plot", "figure")],
        prevent_initial_call=True,
    )
    def update_plot(selected_genes: str, selected_datasets: list, x_axis: str, plot_type: str, 
                   active_tab: str, ter_threshold: int, current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str, str, bool]:
        ctx = callback_context
        if not ctx.triggered or active_tab != "gene-visualization" and ctx.triggered[0]['prop_id'].split('.')[0] != "tabs":
            return no_update, no_update, no_update, no_update
        
        # Skip if tab change to gene-comparison triggered this callback
        if ctx.triggered[0]['prop_id'].split('.')[0] == "tabs" and active_tab == "gene-comparison":
            return no_update, no_update, no_update, no_update
        
        # Check for required selections
        if not selected_genes:
            return {}, "", html.Strong("Please select at least one gene"), True
        if not selected_datasets:
            return {}, "", html.Strong("Please select at least one dataset"), True
            
        # Handle None value when the input is empty   
        if ter_threshold is None:
            ter_threshold = 0
            
        try:
            # Fetch data
            data = fetch_gene_expression_data((selected_genes,), tuple(selected_datasets))
            
            if data.empty:
                return {}, "", html.Strong("No data available for the selected combination"), True
            
            # Ensure TER is numeric
            if 'TER' in data.columns:
                data['TER'] = pd.to_numeric(data['TER'], errors='coerce')
            
            # Filter by TER threshold
            if ter_threshold > 0:
                filtered_data = data[data['TER'] > ter_threshold].copy()
                if filtered_data.empty:
                    return {}, "", html.Strong(f"No data available with TER > {ter_threshold}"), True
                data = filtered_data
            
            # Fill any nulls in x_axis column with 'Unknown', including when all values are null
            if x_axis in data.columns:
                data[x_axis] = data[x_axis].fillna('Unknown')
                
            # Drop any rows with null TPM values as they can't be plotted
            if 'TPM' in data.columns:
                data = data.dropna(subset=['TPM'])
                if data.empty:
                    return {}, "", html.Strong("No non-null TPM values available for the selected data"), True
            
            # Common hover data for all plot types
            hover_cols = ['GeneName', 'DatasetName', 'SubsetName', 'TissueName',
                          'SubstrateType', 'Gender', 'Stage', 'Status',
                          'NhuDifferentiation', 'SampleId', 'TER']
            
            # Create plot with dynamic x-axis and plot type
            if plot_type == "violin":
                fig = px.violin(data, x=x_axis, y='TPM', color="DatasetName", 
                                points="all", hover_data=hover_cols)
            elif plot_type == "box":
                fig = px.box(data, x=x_axis, y='TPM', color="DatasetName", 
                             points="all", hover_data=hover_cols)
            else:  # strip/swarm plot (default)
                fig = px.strip(data, x=x_axis, y='TPM', color="DatasetName", 
                               hover_data=hover_cols)
            
            # Update layout
            plot_title = f"Expression of {(selected_genes)} by {x_axis}"
            if ter_threshold > 0:
                plot_title += f" (TER > {ter_threshold})"
                
            fig.update_layout(
                title=plot_title,
                xaxis_title=x_axis,
                yaxis_title="TPM (Transcripts Per Million)",
                xaxis={'categoryorder': 'total ascending'},
                legend_title_text="Dataset"
            )
            
            return apply_common_styling(fig), "", "", False
            
        except Exception as e:
            return current_figure or {}, "", html.Strong(f"Error generating plot: {str(e)}"), True
    
    @app.callback(
        output=[
            Output("gene-comparison-plot", "figure"),
            Output("error-alert-comp", "children", allow_duplicate=True),
            Output("error-alert-collapse-comp", "is_open", allow_duplicate=True),
        ],
        inputs=[
            Input("gene-comparison-dropdown-1", "value"),
            Input("gene-comparison-dropdown-2", "value"),
            Input("dataset-radio", "value"),
            Input("tabs", "active_tab"),
            Input("ter-input", "value")
        ],
        state=[State("gene-comparison-plot", "figure")],
        prevent_initial_call=True,
    )
    def update_comparison_plot(gene1: str, gene2: str, selected_datasets: list, 
        active_tab: str, ter_threshold: int, current_figure: Dict[str, Any]) -> Tuple[Dict[str, Any], str, bool]:
        ctx = callback_context
        if not ctx.triggered or active_tab != "gene-comparison" and ctx.triggered[0]['prop_id'].split('.')[0] != "tabs":
            return no_update, no_update, no_update
        
        # Skip if tab change to gene-visualization triggered this callback
        if ctx.triggered[0]['prop_id'].split('.')[0] == "tabs" and active_tab == "gene-visualization":
            return no_update, no_update, no_update
        
        # Check for required selections
        if not gene1 or not gene2:
            missing = "first" if not gene1 else "second"
            message = f"Please select the {missing} gene"
            return create_empty_comparison_plot(gene1, gene2, message), html.Strong(message), True
        if gene1 == gene2:
            message = "Please select different genes for comparison"
            return create_empty_comparison_plot(gene1, gene2, message), html.Strong(message), True
        if not selected_datasets:
            message = "Please select at least one dataset"
            return create_empty_comparison_plot(gene1, gene2, message), html.Strong(message), True
        
        # Handle None value when the input is empty
        if ter_threshold is None:
            ter_threshold = 0
            
        try:
            # Fetch and prepare data
            data = fetch_gene_expression_data((gene1, gene2), tuple(selected_datasets))
            
            if data.empty:
                message = "No data available for the selected combination"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
            
            # Ensure TER is numeric
            if 'TER' in data.columns:
                data['TER'] = pd.to_numeric(data['TER'], errors='coerce')
             
            # Filter by TER threshold
            if ter_threshold > 0:
                filtered_data = data[data['TER'] > ter_threshold].copy()
                if filtered_data.empty:
                    message = f"No data available with TER > {ter_threshold}"
                    return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
                data = filtered_data
            
            # Process data for scatter plot
            gene1_data = data[data['GeneName'] == gene1].copy()
            gene2_data = data[data['GeneName'] == gene2].copy()
            
            # Check for empty datasets after filtering
            if gene1_data.empty:
                message = f"No data available for {gene1} with the current filters"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
            if gene2_data.empty:
                message = f"No data available for {gene2} with the current filters"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
            
            # Drop any rows with null TPM values
            gene1_data = gene1_data.dropna(subset=['TPM'])
            gene2_data = gene2_data.dropna(subset=['TPM'])
            
            if gene1_data.empty:
                message = f"No non-null TPM values available for {gene1}"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
            if gene2_data.empty:
                message = f"No non-null TPM values available for {gene2}"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
            
            gene1_count = len(gene1_data)
            gene2_count = len(gene2_data)
            
            # Define metadata columns for hover data
            metadata_columns = ['DatasetName', 'SubsetName', 'TissueName', 'SubstrateType', 
                                'Gender', 'Stage', 'Status', 'NhuDifferentiation', 'TER']
            available_metadata = [col for col in metadata_columns if col in data.columns]
            
            gene1_data = gene1_data.rename(columns={'TPM': f'{gene1}_TPM'})
            gene2_data = gene2_data.rename(columns={'TPM': f'{gene2}_TPM'})
            
            if 'SampleId' not in gene1_data.columns:
                message = "Sample ID information is not available for proper gene comparison"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
            
            # Prepare data for merge
            gene1_cols = ['SampleId'] + available_metadata + [f'{gene1}_TPM']
            gene2_cols = ['SampleId'] + [f'{gene2}_TPM']
            
            gene1_data = gene1_data[gene1_cols].drop_duplicates('SampleId')
            gene2_data = gene2_data[gene2_cols].drop_duplicates('SampleId')
            
            # Merge the dataframes on SampleId
            merged_data = gene1_data.merge(gene2_data, on='SampleId', how='inner')
            matched_count = len(merged_data)
            
            if merged_data.empty:
                diag_message = f"Found {gene1_count} samples for {gene1}, {gene2_count} samples for {gene2}, and 0 matching samples."
                message = f"No matching samples found for both genes. {diag_message}"
                return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True
                
            # Create scatter plot
            hover_data = {'SampleId': True, f'{gene1}_TPM': True, f'{gene2}_TPM': True}
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
            
            # Update layout
            plot_title = f"Gene Comparison: {gene1} vs {gene2}"
            if ter_threshold > 0:
                plot_title += f" (TER > {ter_threshold})"
                
            fig.update_layout(
                title=plot_title,
                xaxis_title=f"{gene1} Expression (TPM)",
                yaxis_title=f"{gene2} Expression (TPM)",
                legend_title_text="Dataset"
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
            
            # Find max value for axis ranges
            max_val = max(
                merged_data[f'{gene1}_TPM'].max(), 
                merged_data[f'{gene2}_TPM'].max()
            )
            
            # Add reference line (y=x)
            """ fig.add_trace(
                go.Scatter(
                    x=[0, max_val],
                    y=[0, max_val],
                    mode='lines',
                    line=dict(color='rgba(0,0,0,0.5)', dash='dash', width=2),
                    name='1:1 Line (y=x)'
                )
            ) """
            
            # Add regression line if there are enough data points
            if len(merged_data) > 1:
                x_values = merged_data[f'{gene1}_TPM'].values
                y_values = merged_data[f'{gene2}_TPM'].values
                
                #print(f"x_values: {x_values}")
                #print(f"y_values: {y_values}")
                
                # Calculate Pearson correlation
                pearson_corr, p_value = stats.pearsonr(x_values, y_values)
                
                # Calculate Spearman correlation
                spearman_corr, spearman_p = stats.spearmanr(x_values, y_values)
                
                # Calculate Pearson correlation for log10(TPM+1)
                log_x = np.log10(x_values + 1)
                log_y = np.log10(y_values + 1)
                pearson_corr_log, p_value_log = stats.pearsonr(log_x, log_y)
                
                # Standard regression line calculation
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
                r_squared = r_value**2
                
                # Add regression line
                x_reg = np.array([0, max_val])
                y_reg = intercept + slope * x_reg
                
                fig.add_trace(
                    go.Scatter(
                        x=x_reg,
                        y=y_reg,
                        mode='lines',
                        line=dict(color='rgba(255,0,0,0.7)', width=2),
                        name='Regression Line'
                    )
                )
                
                # Create a string with all correlation information
                correlation_text = (
                    f"Pearson: {pearson_corr:.3f}, "
                    f"Pearson log10(TPM+1): {pearson_corr_log:.3f}, "
                    f"Spearman: {spearman_corr:.3f}"
                )
                
                # Add regression equation and correlation coefficients to title
                regression_text = f"(y = {slope:.2f}x + {intercept:.2f}, R² = {r_squared:.2f})"
                fig.update_layout(title=f"{plot_title} - {regression_text}")
                
                # Add correlation coefficients as an annotation at the bottom of the plot
                fig.add_annotation(
                    xref="paper", yref="paper",
                    x=0.5, y=0,
                    text=correlation_text,
                    showarrow=False,
                    font=dict(size=12),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="rgba(0,0,0,0.2)",
                    borderwidth=1,
                    borderpad=4,
                    align="center"
                )
            
            return apply_common_styling(fig), "", False
                
        except Exception as e:
            message = f"Error generating comparison plot: {str(e)}"
            return create_empty_comparison_plot(gene1, gene2, message, ter_threshold), html.Strong(message), True

    def create_empty_comparison_plot(gene1, gene2, message, ter_threshold=None):
        """Helper function to create an empty comparison plot with appropriate labels"""
        fig = px.scatter(
            x=[0], y=[0],  # Dummy data that won't be visible
            labels={'x': f"{gene1 or 'Gene 1'} Expression (TPM)", 
                   'y': f"{gene2 or 'Gene 2'} Expression (TPM)"}
        )
        
        # Build an appropriate title
        if gene1 and gene2:
            title = f"Gene Comparison: {gene1} vs {gene2}"
        elif gene1:
            title = f"Gene Comparison: {gene1} vs (select second gene)"
        elif gene2:
            title = f"Gene Comparison: (select first gene) vs {gene2}"
        else:
            title = "Gene Comparison (select genes)"
            
        # Add TER threshold to title if provided
        if ter_threshold and ter_threshold > 0:
            title += f" (TER > {ter_threshold})"
            
        # Add the error context to title
        title += f" - {message}"
        
        fig.update_layout(
            title=title,
            xaxis_title=f"{gene1 or 'Gene 1'} Expression (TPM)",
            yaxis_title=f"{gene2 or 'Gene 2'} Expression (TPM)"
        )
        
        # Add placeholder for correlation coefficients (will be empty in error state)
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.5, y=0,
            text="No correlation data available",
            showarrow=False,
            font=dict(size=12, color="rgba(150,150,150,0.8)"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
            borderpad=4,
            align="center",
            opacity=0.7
        )
        
        # Hide the dummy point
        fig.update_traces(marker={'opacity': 0})
        
        return apply_common_styling(fig)
