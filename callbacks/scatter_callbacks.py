from dash import callback, Output, Input , html
import plotly.express as px
import plotly.graph_objects as go
from visualizations.plots.scatter import create_scatter_plot
import globals

data_processor = globals.data_processor  # Access the global data processor

@callback(
    Output('scatter-plot', 'figure'),
    Output('depth-summary', 'children'),
    [Input('scatter-year-range', 'value'),
     Input('scatter-country-filter', 'value')]
)
def update_scatter_plot(year_range, country_filter):
    start_year, end_year = year_range if year_range else (None, None)

    fig, counts = create_scatter_plot(
        data_processor,
        country_filter=country_filter,
        start_year=start_year,
        end_year=end_year
    )

    summary_text = f"""
    Total Earthquakes: {counts['total']}  
    Shallow (≤70 km): {counts['shallow']}  
    Intermediate (70–300 km): {counts['intermediate']}  
    Deep (>300 km): {counts['deep']}
    """

    return fig, html.Pre(summary_text, style={'whiteSpace': 'pre-wrap'})
