from dash import html, dcc

def get_scatter_section(data_processor):
    countries = [{'label': 'All Countries', 'value': 'all'}] + [
    {'label': country, 'value': country}
    for country in sorted(
        data_processor.get_filtered_data()['country']
        .dropna()
        .unique()
    )
]



    
    return html.Div([
        html.H3("Depth vs Magnitude Scatter Plot", style={'color': '#2c3e50'}),
        html.P(
            "Depth plays an important role in the impact of an earthquake. This scatter plot shows how depth and magnitude vary together.",
            style={'color': '#2c3e50'}
        ),
        html.Div([
            html.Label("Year Range:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='scatter-year-range',
                min=1900,
                max=2023,
                step=1,
                value=[2020, 2023],
                marks={1900: '1900', 1950: '1950', 2000: '2000', 2023: '2023'},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'marginBottom': '20px'}),
        html.Div([
            html.Label("Country Filter:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='scatter-country-filter',
                options=countries,
                value='all'
            )
        ], style={'marginBottom': '20px'}),
        dcc.Graph(id='scatter-plot', style={'height': '500px'}),
        html.Div(id='depth-summary', style={'marginTop': '15px', 'fontWeight': 'bold', 'color': '#2c3e50'})
    ], id='scatter-section', style={'marginBottom': '30px'})
