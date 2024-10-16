import os
import webbrowser
import folium
import logging

# Configure logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_world_map(data):
    """Creates a world map with markers for the provided country data.

    Args:
        data (dict): Dictionary containing country names and their coordinates.

    Returns:
        folium.Map: A folium map object with markers.
    """
    # Initialize a folium map centered at an average location
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    # Adding markers to the map
    for index, country in enumerate(data["Country"]):
        latitude = data["Latitude"][index]
        longitude = data["Longitude"][index]

        # Validate latitude and longitude
        if is_valid_coordinate(latitude, longitude):
            folium.Marker(
                location=[latitude, longitude],
                popup=country,
                icon=folium.Icon(color='blue')
            ).add_to(world_map)
            logging.info(f"Added marker for {country} at ({latitude}, {longitude}).")
        else:
            logging.warning(f"Invalid coordinates for {country}: ({latitude}, {longitude})")

    return world_map

def is_valid_coordinate(latitude, longitude):
    """Validates the latitude and longitude values.

    Args:
        latitude (float): Latitude value to validate.
        longitude (float): Longitude value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180

def save_map(map_object, filename):
    """Saves the folium map object to an HTML file.

    Args:
        map_object (folium.Map): The map object to save.
        filename (str): The filename for the saved HTML file.
    """
    try:
        map_object.save(filename)
        logging.info(f"Map saved as '{filename}'.")
    except Exception as e:
        logging.error(f"Error saving map: {e}")

def open_map_in_browser(filename):
    """Opens the saved HTML map file in the default web browser.

    Args:
        filename (str): The filename of the HTML map file.
    """
    try:
        webbrowser.open('file://' + os.path.abspath(filename))
        logging.info(f"Opened map in browser: '{filename}'.")
    except Exception as e:
        logging.error(f"Error opening map in browser: {e}")

def map_main():
    """Main function to create, save, and open the world map."""
    data = {
        "Country": ["USA", "Canada", "Brazil", "UK", "Germany", "Australia"],
        "Latitude": [37.0902, 56.1304, -14.2350, 55.3781, 51.1657, -25.2744],
        "Longitude": [-95.7129, -106.3468, -51.9253, -3.4360, 10.4515, 133.7751]
    }

    world_map = create_world_map(data)
    html_file = "docs/world_map.html"
    save_map(world_map, html_file)
    open_map_in_browser(html_file)
