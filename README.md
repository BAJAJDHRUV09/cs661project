# CS661: Earthquake Data Visualization Project

## Group 15 - Interactive Earthquake Analysis Tool

### Project Overview
This project creates an interactive standalone tool to explore and analyze global earthquake data from 1990-2023. The tool provides visualizations to understand earthquake patterns, identify high-risk regions, and analyze temporal trends.

### Features
- **Time Series Analysis**: Earthquake trends over time with interactive filtering
- **Global Risk Map**: Choropleth map showing earthquake frequency and intensity by region
- **Country Focus**: Detailed local analysis with zoom capabilities
- **Scatter Plot Analysis**: Depth vs Magnitude relationships
- **Epicentre Impact**: Visual impact zones and significance analysis

### Tech Stack
- **Data Processing**: Python, Pandas, NumPy
- **Visualization**: Plotly, Dash
- **Database**: SQLite (optional)

### Team Members & Responsibilities
- **Data Aggregation, Cleaning & Trend Analysis**: Daksh Agrawal (230337), Jaini Patel (230494)
- **Time Series Analysis**: Neel D Jadia (230688)
- **Country Isolation & Zoom Interaction**: Dharajiya Yug (230362)
- **Risk Analysis**: Chatla Sowmya Sri (200293)
- **Scatter Plot**: Shivanee Shrivas (230974)
- **Global Map & Epicentre Impact**: Parv Mehta (230741), Dhruv Bajaj (230365), Bipin Kumar Jaiswal (230300) 

### Installation
1. Clone the repository
2. Set up virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate  On macOS/Linux ` or `venv\Scripts\activate  On Windows`
4. Install dependencies: `pip install -r requirements.txt`
5. Download the earthquake dataset from Kaggle
6. Run the application: `python app.py`

### Data Sources
- All the Earthquakes Dataset (1990–2023) from Kaggle
- USGS Significant Earthquakes Catalog

### Project Structure
```
661_project/
├── app.py            # Main Dash application 
├── callbacks         # Folder for all Dash callback functions that handle interactivity 
├── components        # Reusable UI components like dropdowns, graphs, sliders, etc.
├── data/             # Folder for cleaned and processed data files (e.g., CSV, GeoJSON) 
├── src/              # Core logic modules: data loading, preprocessing, analytics, utilities 
├── visualizations    # Static plots, maps, or notebooks used for EDA and reporting
├── requirements.txt  # List of required Python packages for setting up the environment
└── README.md         # Project documentation with setup instructions and usage guide
``` 
