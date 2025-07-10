from dash import callback, Output, Input
from visualizations.plots.time_series import create_time_series_plot
import globals
import calendar
import pandas as pd  # Make sure this is imported

data_processor = globals.data_processor  # Access the global data processor

@callback(
    Output('timeseries-plot', 'figure'),
    [Input('timeseries-year', 'value'),
     Input('timeseries-month', 'value')]
)
def update_timeseries_plot(selected_year, selected_month):
    if selected_month == "all":
        start_str = f"{selected_year}-01-01"
        end_str = f"{selected_year}-12-31"
    else:
        month = int(selected_month)
        last_day = calendar.monthrange(int(selected_year), month)[1]
        start_str = f"{selected_year}-{month:02d}-01"
        end_str = f"{selected_year}-{month:02d}-{last_day}"

    # Convert to tz-aware Timestamps
    start_date = pd.to_datetime(start_str).tz_localize("UTC")
    end_date = pd.to_datetime(end_str).tz_localize("UTC")

    return create_time_series_plot(
        data_processor=data_processor,
        start_date=start_date,
        end_date=end_date
    )
