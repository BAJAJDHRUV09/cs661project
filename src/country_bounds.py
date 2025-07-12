# country_bounds.py
from typing import Optional, Tuple
import math
# Latitude and longitude bounding boxes for countries
# Format: (min_lat, max_lat, min_lon, max_lon)
COUNTRY_BOUNDS = {
    "Afghanistan": (29.3772, 38.4834, 60.5284, 75.1580),
    "Albania": (39.6249, 42.6612, 19.3045, 21.0574),
    "Algeria": (18.9764, 37.1184, -8.6739, 11.9986),
    "Argentina": (-55.05, -21.78, -73.58, -53.64),
    "Australia": (-43.0031, -10.6682, 113.3389, 153.5695),
    "Austria": (46.3723, 49.0205, 9.5309, 17.1606),
    "Bangladesh": (20.59, 26.63, 88.01, 92.68),
    "Belgium": (49.4970, 51.5052, 2.5411, 6.4074),
    "Brazil": (-33.7507, 5.2718, -73.9872, -34.7939),
    "Canada": (41.6766, 83.1139, -141.0, -52.6363),
    "Chile": (-56.0, -17.5, -75.7, -66.4),
    "China": (18.0, 53.56, 73.66, 135.05),
    "Colombia": (-4.23, 13.38, -79.0, -66.87),
    "Czech Republic": (48.55, 51.06, 12.09, 18.86),
    "Denmark": (54.56, 57.75, 8.07, 15.19),
    "Egypt": (22.0, 31.67, 25.0, 35.0),
    "Finland": (59.81, 70.09, 20.55, 31.59),
    "France": (41.36, 51.09, -5.14, 9.56),
    "Germany": (47.27, 55.06, 5.87, 15.04),
    "Greece": (34.8, 41.75, 19.35, 28.25),
    "India": (6.55, 35.67, 68.11, 97.25),
    "Indonesia": (-10.0, 6.1, 95.0, 141.0),
    "Iran": (24.0, 39.8, 44.0, 63.3),
    "Iraq": (29.06, 37.38, 38.79, 48.57),
    "Italy": (36.0, 47.1, 6.6, 18.5),
    "Japan": (24.396308, 45.551483, 122.93457, 153.986672),
    "Malaysia": (0.85, 7.35, 99.64, 119.27),
    "Mexico": (14.5, 32.7, -117.1, -86.7),
    "Nepal": (26.3, 30.4, 80.0, 89.0),
    "New Zealand": (-47.3, -34.0, 166.5, 178.6),
    "Norway": (57.98, 71.18, 4.09, 31.1),
    "Pakistan": (23.7, 37.0, 60.9, 77.0),
    "Peru": (-18.35, -0.04, -81.33, -68.65),
    "Philippines": (4.6, 21.3, 116.9, 126.6),
    "Poland": (49.0, 54.84, 14.12, 24.15),
    "Portugal": (36.96, 42.15, -9.5, -6.19),
    "Romania": (43.61, 48.27, 20.26, 29.7),
    "Russia": (41.2, 81.86, 19.66, 190.0),
    "Saudi Arabia": (16.3, 32.2, 34.5, 55.7),
    "South Africa": (-34.83, -22.13, 16.45, 32.89),
    "South Korea": (33.0, 43.0, 124.0, 132.0),
    "Spain": (36.0, 43.79, -9.3, 3.33),
    "Sri Lanka": (5.9, 9.8, 79.4, 81.9),
    "Sweden": (55.34, 69.06, 11.1, 24.16),
    "Switzerland": (45.82, 47.81, 5.96, 10.49),
    "Syria": (32.0, 37.3, 35.7, 42.0),
    "Thailand": (5.61, 20.46, 97.35, 105.64),
    "Turkey": (35.8, 42.1, 25.7, 44.8),
    "Ukraine": (44.0, 52.4, 22.0, 40.2),
    "United Arab Emirates": (22.6, 26.1, 51.5, 56.4),
    "United Kingdom": (49.9, 60.9, -8.6, 1.8),
    "United States": (24.396308, 49.384358, -125.0, -66.93457),
    "Vietnam": (8.2, 23.4, 102.1, 109.5)
}

def get_country_bounds(country: str) -> Optional[Tuple[float, float, float, float]]:
    return COUNTRY_BOUNDS.get(country)

def estimate_zoom_from_bounds(bounds: Tuple[float, float, float, float]) -> float:
    if not bounds:
        return 1.0

    lat_range = abs(bounds[1] - bounds[0])
    lon_range = abs(bounds[3] - bounds[2])
    max_range = max(lat_range, lon_range)

    # Avoid log(0)
    max_range = max(max_range, 1e-6)

    # Zoom level: approximate log scale inverse relation
    # tweak the constants to fit your zoom needs
    zoom = 12 - math.log2(max_range)

    # Clamp between 1 and 12 (for typical world-to-city level zoom)
    return max(1.0, min(zoom, 12.0))
