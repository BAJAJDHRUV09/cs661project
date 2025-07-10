def get_magnitude_color(mag):
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
