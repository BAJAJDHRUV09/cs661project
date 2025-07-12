import dash
from dash import callback
from components.layout import create_layout
from src.data_processor import DataProcessor
import globals
import warnings
warnings.filterwarnings('ignore')

app = dash.Dash(__name__, title="Earthquake Data Visualization")
app.config.suppress_callback_exceptions = True
globals.data_processor = DataProcessor()
data_processor = globals.data_processor
app.layout = create_layout(data_processor)

# Register callbacks
from callbacks import layout_toggle, navigation, map_callbacks, scatter_callbacks, timeseries_callbacks , riskmap_callbacks, content_switch , timeseries_toggle , country_options_callbacks, country_focus_callbacks , country_focus_toggle
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
