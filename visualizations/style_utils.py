import numpy as np

def get_magnitude_color(mag):
    """
    Color scheme from light yellow (lower intensity) to bright red (higher intensity).
    Light yellow for lower magnitude, bright red for higher magnitude.
    """
    if mag < 6.0:
        return '#fff7bc'  # Light yellow (lowest intensity)
    elif mag < 6.5:
        return '#fec44f'  # Light orange-yellow (low intensity)
    elif mag < 7.0:
        return '#fe9929'  # Orange (medium intensity)
    elif mag < 7.5:
        return '#d7301f'  # Red-orange (high intensity)
    else:
        return '#b30000'  # Bright red (highest intensity)

def get_magnitude_color_old(mag):
    """Original color function for reference"""
    if mag < 6.0:
        return '#ffb86c'  # Dracula orange
    elif mag < 6.5:
        return '#ff79c6'  # Dracula pink
    elif mag < 7.0:
        return '#ff5555'  # Dracula red
    elif mag < 7.5:
        return '#bd93f9'  # Dracula purple
    else:
        return '#ff5555'  # Dracula red
