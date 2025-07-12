from dash import html, dcc
import pandas as pd
import numpy as np
def get_timeseries_section(data_processor):
    df = data_processor.get_filtered_data()
    years = sorted(df['year'].dropna().unique())
    countries = sorted(df['country'].dropna().unique())
    year_max = max(years) if years else 2023 
    year_min = min(years) if years else 1900
    num_marks = 7
    mark_years = np.linspace(year_min, year_max, num=num_marks, dtype=int)
    return html.Div([
        html.H3("Earthquake Time Series Analysis", style={'color': '#2c3e50'}),

        html.Div([
            html.Label("Select View Mode:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='timeseries-view-mode',
                options=[
                    {'label': 'Single Year View', 'value': 'single'},
                    {'label': 'Year Range View', 'value': 'range'}
                ],
                value='single',
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            )
        ], style={'marginBottom': '15px'}),

        # Single Year Controls
        html.Div([
            html.Div([
                html.Label("Year:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='timeseries-year',
                    options=[{'label': str(y), 'value': int(y)} for y in years],
                    value=int(years[-1]) if years else 2023
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
        ], id='single-controls', style={'marginBottom': '20px'}),

        # Year Range Controls (hidden by default) 
        html.Div([
            html.Label("Year Range:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='timeseries-year-range',
                min=int(min(years)),
                max=int(max(years)),
                step=1,
                value=[year_max - 5, year_max],  # default range (last 5 years)
                marks={int(y): str(y) for y in mark_years},
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], id='range-controls', style={'marginBottom': '20px', 'display': 'none'}),

        html.Div([
            html.Label("Country (optional):", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='timeseries-country',
                options=[{'label': c, 'value': c} for c in countries],
                placeholder='Select Country (Optional)'
            )
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Label("Show Options:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.Checklist(
                id='timeseries-options',
                options=[
                    {'label': 'Cumulative View', 'value': 'cumulative'},
                    {'label': '5-Year Moving Average', 'value': 'moving_avg'}
                ],
                value=[],
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            )
        ], style={'marginBottom': '20px'}),

        # First plot - Earthquake Count Metrics
        html.Div([
            html.H4("Earthquake Count Trends", style={'color': '#2c3e50', 'marginBottom': '10px'}),
            dcc.Graph(id='timeseries-count-plot', style={'height': '600px'})
        ], style={'marginBottom': '30px'}),

        # Second plot - Magnitude Data
        html.Div([
            html.H4("Magnitude Trends", style={'color': '#2c3e50', 'marginBottom': '10px'}),
            dcc.Graph(id='timeseries-magnitude-plot', style={'height': '600px'})
        ], style={'marginBottom': '30px'})
    ], id='timeseries-section', style={'marginBottom': '30px'})
