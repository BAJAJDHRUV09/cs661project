from dash import html, dcc

def get_timeseries_section(data_processor):
    years = sorted(data_processor.get_filtered_data()['year'].unique())

    return html.Div([
        html.H3("Earthquake Time Series Analysis", style={'color': '#2c3e50'}),
        html.Div([
            html.Div([
                html.Label("Year:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='timeseries-year',
                    options=[{'label': str(y), 'value': y} for y in years],
                    value=2023
                )
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
            html.Div([
                html.Label("Month:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='timeseries-month',
                    options=[
                        {'label': 'All Months', 'value': 'all'},
                        *[{'label': name, 'value': i} for i, name in enumerate(
                            ['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 'December'], 1)]
                    ],
                    value='all'
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'}),
        dcc.Graph(id='timeseries-plot', style={'height': '500px'})
    ], id='timeseries-section', style={'marginBottom': '30px'})
