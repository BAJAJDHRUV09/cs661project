import dash
from dash import dcc, html, Input, Output, callback, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Import custom modules
from src.data_processor import DataProcessor
from src.visualizations import create_global_earthquake_map

# Initialize the Dash app
app = dash.Dash(__name__, title="Earthquake Data Visualization")
app.config.suppress_callback_exceptions = True

# Initialize data processor
data_processor = DataProcessor()

# App layout
app.layout = html.Div([
    # Sidebar toggle button
    html.Button(
        "☰",
        id="sidebar-toggle",
        style={
            'position': 'fixed',
            'top': '20px',
            'left': '20px',
            'zIndex': 1000,
            'fontSize': '24px',
            'padding': '10px 15px',
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
        }
    ),
    
    # Sidebar
    html.Div([
        html.Div([
            html.H3("Earthquake Analysis", style={'color': '#2c3e50', 'marginBottom': '20px'}),
            
            # Traditional list menu
            html.Div([
                html.H4("Select Visualization:", style={'color': '#2c3e50', 'marginBottom': '15px'}),
                
                # List items
                html.Div([
                    html.Button(
                        "Global Map",
                        id='btn-map',
                        style={
                            'width': '100%',
                            'textAlign': 'left',
                            'padding': '12px 15px',
                            'marginBottom': '8px',
                            'backgroundColor': '#2c3e50',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer',
                            'fontSize': '14px'
                        }
                    ),
                    html.Button(
                        "Depth vs Magnitude Scatter Plot",
                        id='btn-scatter',
                        style={
                            'width': '100%',
                            'textAlign': 'left',
                            'padding': '12px 15px',
                            'marginBottom': '8px',
                            'backgroundColor': '#ecf0f1',
                            'color': '#2c3e50',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer',
                            'fontSize': '14px'
                        }
                    ),
                    html.Button(
                        "Time Series Analysis",
                        id='btn-timeseries',
                        style={
                            'width': '100%',
                            'textAlign': 'left',
                            'padding': '12px 15px',
                            'marginBottom': '8px',
                            'backgroundColor': '#ecf0f1',
                            'color': '#2c3e50',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer',
                            'fontSize': '14px'
                        }
                    )
                ])
            ], style={'padding': '20px'})
        ], style={'padding': '20px'})
    ], id="sidebar", style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '300px',
        'height': '100vh',
        'backgroundColor': 'white',
        'boxShadow': '2px 0 5px rgba(0,0,0,0.1)',
        'zIndex': 999,
        'transform': 'translateX(-100%)',
        'transition': 'transform 0.3s ease-in-out',
        'overflowY': 'auto'
    }),
    
    # Main content (shifted when sidebar is open)
    html.Div([
        # Main visualization container
        html.Div([
            # Map container
            html.Div([
                dcc.Graph(
                    id='global-map', 
                    style={
                        'height': '600px',
                        'width': '90%',
                        'minWidth': '1000px',
                        'minHeight': '500px',
                        'display': 'block',
                        'margin': '0 auto'
                    },
                    config={
                        'displayModeBar': True,   # Show zoom controls
                        'scrollZoom': True,       # Allow scroll zoom
                        'showTips': True          # Show tips
                    }
                )
            ], style={
                'width': '100%',
                'minWidth': '1200px',
                'minHeight': '700px',
                'marginBottom': '20px',
                'overflow': 'hidden',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center'
            }),
            
            # Year slider container - centered below map
            html.Div([
                html.Div([
                    html.Label(
                        "Year: ", 
                        style={
                            'marginRight': '15px', 
                            'fontWeight': 'bold',
                            'fontSize': '16px',
                            'color': '#2c3e50'  # Dark text for white background
                        }
                    ),
                    dcc.Slider(
                        id='year-slider',
                        min=1900,
                        max=2023,
                        step=1,
                        value=2023,
                        marks={
                            1900: '1900',
                            1920: '1920', 
                            1940: '1940',
                            1960: '1960',
                            1980: '1980',
                            2000: '2000',
                            2020: '2020',
                            2023: '2023'
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                        included=False
                    )
                ], style={
                    'width': '800px',
                    'margin': '0 auto',
                    'padding': '20px',
                    'backgroundColor': '#f8f9fa',  # Light background
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'border': '1px solid #dee2e6'  # Light border
                })
            ], style={
                'width': '100%',
                'textAlign': 'center',
                'marginBottom': '20px'
            })
        ], style={
            'width': '100%',
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px',
            'transition': 'margin-left 0.3s ease-in-out'
        }, id="main-content"),
        
        # Additional visualizations container
        html.Div([
            # Scatter plot controls
            html.Div([
                html.H3("Depth vs Magnitude Scatter Plot", style={'color': '#2c3e50', 'marginBottom': '20px'}),
                html.P(
                    "Depth plays an important role in the impact of an earthquake. This scatter plot shows "
                    "how depth and magnitude vary together and helps identify whether shallow or deep quakes "
                    "are more common in a region.",
                    style={'color': '#2c3e50', 'lineHeight': '1.6', 'marginBottom': '20px'}
                ),
                
                # Filters
                html.Div([
                    html.Div([
                        html.Label("Year Range:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                        dcc.RangeSlider(
                            id='scatter-year-range',
                            min=1900,
                            max=2023,
                            step=1,
                            value=[2020, 2023],
                            marks={
                                1900: '1900',
                                1950: '1950',
                                2000: '2000',
                                2023: '2023'
                            },
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], style={'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Label("Country Filter:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='scatter-country-filter',
                            options=[{'label': 'All Countries', 'value': 'all'}] + 
                                   [{'label': str(country), 'value': str(country)} for country in 
                                    sorted(data_processor.get_filtered_data()['Place'].dropna().unique())],
                            value='all',
                            style={'marginTop': '5px'}
                        )
                    ], style={'marginBottom': '20px'})
                ], style={'marginBottom': '20px'}),
                
                # Scatter plot
                dcc.Graph(
                    id='scatter-plot',
                    style={'height': '500px'}
                )
            ], id='scatter-section', style={'display': 'none', 'marginBottom': '30px'}),
            
            # Time series controls
            html.Div([
                html.H3("Earthquake Time Series Analysis", style={'color': '#2c3e50', 'marginBottom': '20px'}),
                
                # Time filters
                html.Div([
                    html.Div([
                        html.Label("Year:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='timeseries-year',
                            options=[{'label': str(year), 'value': year} for year in 
                                    sorted(data_processor.get_filtered_data()['year'].unique())],
                            value=2023,
                            style={'marginTop': '5px'}
                        )
                    ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
                    
                    html.Div([
                        html.Label("Month:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='timeseries-month',
                            options=[
                                {'label': 'All Months', 'value': 'all'},
                                {'label': 'January', 'value': 1},
                                {'label': 'February', 'value': 2},
                                {'label': 'March', 'value': 3},
                                {'label': 'April', 'value': 4},
                                {'label': 'May', 'value': 5},
                                {'label': 'June', 'value': 6},
                                {'label': 'July', 'value': 7},
                                {'label': 'August', 'value': 8},
                                {'label': 'September', 'value': 9},
                                {'label': 'October', 'value': 10},
                                {'label': 'November', 'value': 11},
                                {'label': 'December', 'value': 12}
                            ],
                            value='all',
                            style={'marginTop': '5px'}
                        )
                    ], style={'width': '48%', 'display': 'inline-block'})
                ], style={'marginBottom': '20px'}),
                
                # Time series plot
                dcc.Graph(
                    id='timeseries-plot',
                    style={'height': '500px'}
                )
            ], id='timeseries-section', style={'display': 'none', 'marginBottom': '30px'})
        ], style={
            'width': '100%',
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px'
        }),
        
        # Footer
        html.Div([
            html.P("CS661 Project - Group 15",
                   style={'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '30px'})
        ])
    ], style={
        'padding': '20px', 
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': 'white',  # White background
        'minHeight': '100vh',
        'color': '#2c3e50'  # Dark text for white background
    })
], id="app-container")

# Callback for sidebar toggle
@callback(
    [Output("sidebar", "style"),
     Output("main-content", "style")],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "style"),
     State("main-content", "style")]
)
def toggle_sidebar(n_clicks, sidebar_style, main_style):
    if n_clicks is None:
        return sidebar_style, main_style
    
    if sidebar_style.get('transform') == 'translateX(0px)':
        # Close sidebar
        sidebar_style['transform'] = 'translateX(-100%)'
        main_style['marginLeft'] = '0px'
    else:
        # Open sidebar
        sidebar_style['transform'] = 'translateX(0px)'
        main_style['marginLeft'] = '300px'
    
    return sidebar_style, main_style

# Callback for the global map
@callback(
    Output('global-map', 'figure'),
    [Input('year-slider', 'value')]
)
def update_global_map(selected_year):
    return create_global_earthquake_map(data_processor, selected_year=selected_year)

# Callback to update button styles
@callback(
    [Output('btn-map', 'style'),
     Output('btn-scatter', 'style'),
     Output('btn-timeseries', 'style')],
    [Input('btn-map', 'n_clicks'),
     Input('btn-scatter', 'n_clicks'),
     Input('btn-timeseries', 'n_clicks')]
)
def update_button_styles(btn_map, btn_scatter, btn_timeseries):
    # Default styles
    map_style = {
        'width': '100%',
        'textAlign': 'left',
        'padding': '12px 15px',
        'marginBottom': '8px',
        'backgroundColor': '#ecf0f1',
        'color': '#2c3e50',
        'border': 'none',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'fontSize': '14px'
    }
    
    scatter_style = map_style.copy()
    timeseries_style = map_style.copy()
    
    # Determine which button was clicked
    if btn_map:
        map_style['backgroundColor'] = '#2c3e50'
        map_style['color'] = 'white'
    elif btn_scatter:
        scatter_style['backgroundColor'] = '#2c3e50'
        scatter_style['color'] = 'white'
    elif btn_timeseries:
        timeseries_style['backgroundColor'] = '#2c3e50'
        timeseries_style['color'] = 'white'
    else:
        # Default to map selected
        map_style['backgroundColor'] = '#2c3e50'
        map_style['color'] = 'white'
    
    return map_style, scatter_style, timeseries_style

# Callback to show/hide sections based on visualization selection
@callback(
    [Output('scatter-section', 'style'),
     Output('timeseries-section', 'style')],
    [Input('btn-map', 'n_clicks'),
     Input('btn-scatter', 'n_clicks'),
     Input('btn-timeseries', 'n_clicks')]
)
def update_visualization_display(btn_map, btn_scatter, btn_timeseries):
    # Hide all sections first
    scatter_style = {'display': 'none', 'marginBottom': '30px'}
    timeseries_style = {'display': 'none', 'marginBottom': '30px'}
    
    # Determine which section to show
    if btn_scatter:
        scatter_style = {'display': 'block', 'marginBottom': '30px'}
    elif btn_timeseries:
        timeseries_style = {'display': 'block', 'marginBottom': '30px'}
    # If btn_map or no button clicked, show map (default)
    
    return scatter_style, timeseries_style

# Callback for scatter plot
@callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-year-range', 'value'),
     Input('scatter-country-filter', 'value')]
)
def update_scatter_plot(year_range, country_filter):
    data = data_processor.get_filtered_data()
    
    # Filter by year range
    if year_range:
        data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])]
    
    # Filter by country
    if country_filter and country_filter != 'all':
        data = data[data['Place'].str.contains(country_filter, case=False, na=False)]
    
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for selected filters",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(height=500)
        return fig
    
    fig = px.scatter(
        data, 
        x='depth', 
        y='mag', 
        color='mag',
        hover_data=['Place', 'year'],
        title="Depth vs Magnitude Relationship",
        labels={'depth': 'Depth (km)', 'mag': 'Magnitude'},
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2c3e50'),
        height=500
    )
    
    return fig

# Callback for time series plot
@callback(
    Output('timeseries-plot', 'figure'),
    [Input('timeseries-year', 'value'),
     Input('timeseries-month', 'value')]
)
def update_timeseries_plot(selected_year, selected_month):
    data = data_processor.get_filtered_data()
    
    # Filter by year
    if selected_year:
        data = data[data['year'] == selected_year]
    
    # Filter by month
    if selected_month and selected_month != 'all':
        data = data[data['month'] == selected_month]
    
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for selected time period",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(height=500)
        return fig
    
    # Group by day and count earthquakes
    if selected_month and selected_month != 'all':
        # Daily counts for specific month
        daily_counts = data.groupby('day').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(f"{selected_year}-{selected_month:02d}-{daily_counts['day']:02d}")
        x_col = 'date'
        title = f"Daily Earthquake Counts - {selected_year}, Month {selected_month}"
    else:
        # Monthly counts for the year
        monthly_counts = data.groupby('month').size().reset_index(name='count')
        monthly_counts['month_name'] = monthly_counts['month'].map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        x_col = 'month_name'
        title = f"Monthly Earthquake Counts - {selected_year}"
    
    if selected_month and selected_month != 'all':
        fig = px.bar(daily_counts, x=x_col, y='count', title=title)
    else:
        fig = px.bar(monthly_counts, x=x_col, y='count', title=title)
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2c3e50'),
        height=500,
        xaxis_title="Time Period",
        yaxis_title="Number of Earthquakes"
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050) 