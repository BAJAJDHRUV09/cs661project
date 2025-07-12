from dash import callback, Output, Input
from visualizations.plots.time_series import create_count_time_series_plot, create_magnitude_time_series_plot
import globals
import calendar
import pandas as pd

data_processor = globals.data_processor

@callback(
    Output('timeseries-count-plot', 'figure'),
    [
        Input('timeseries-view-mode', 'value'),
        Input('timeseries-year', 'value'),
        Input('timeseries-month', 'value'),
        Input('timeseries-year-range', 'value'),
        Input('timeseries-country', 'value'),
        Input('timeseries-options', 'value')
    ]
)
def update_count_timeseries_plot(mode, year, month, year_range, country, options):
    show_cumulative = 'cumulative' in options
    show_moving_avg = 'moving_avg' in options

    if mode == 'single':
        if month == "all":
            start_str = f"{year}-01-01"
            end_str = f"{year}-12-31"
        else:
            last_day = calendar.monthrange(year, int(month))[1]
            start_str = f"{year}-{int(month):02d}-01"
            end_str = f"{year}-{int(month):02d}-{last_day}"
    else:
        start_str = f"{year_range[0]}-01-01"
        end_str = f"{year_range[1]}-12-31"

    start_date = pd.to_datetime(start_str).tz_localize("UTC")
    end_date = pd.to_datetime(end_str).tz_localize("UTC")

    return create_count_time_series_plot(
        data_processor=data_processor,
        start_date=start_date,
        end_date=end_date,
        country=country,
        show_moving_avg=show_moving_avg,
        show_cumulative=show_cumulative,
        mode=mode 
    )

@callback(
    Output('timeseries-magnitude-plot', 'figure'),
    [
        Input('timeseries-view-mode', 'value'),
        Input('timeseries-year', 'value'),
        Input('timeseries-month', 'value'),
        Input('timeseries-year-range', 'value'),
        Input('timeseries-country', 'value'),
        Input('timeseries-options', 'value')
    ]
)
def update_magnitude_timeseries_plot(mode, year, month, year_range, country, options):
    show_moving_avg = 'moving_avg' in options

    if mode == 'single':
        if month == "all":
            start_str = f"{year}-01-01"
            end_str = f"{year}-12-31"
        else:
            last_day = calendar.monthrange(year, int(month))[1]
            start_str = f"{year}-{int(month):02d}-01"
            end_str = f"{year}-{int(month):02d}-{last_day}"
    else:
        start_str = f"{year_range[0]}-01-01"
        end_str = f"{year_range[1]}-12-31"

    start_date = pd.to_datetime(start_str).tz_localize("UTC")
    end_date = pd.to_datetime(end_str).tz_localize("UTC")

    return create_magnitude_time_series_plot(
        data_processor=data_processor,
        start_date=start_date,
        end_date=end_date,
        country=country,
        show_moving_avg=show_moving_avg,
        mode=mode 
    )
