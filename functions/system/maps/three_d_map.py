import pydeck as pdk
import webbrowser


def create_three_d_map(longitude, latitude):
    # Define your data with custom coordinates and elevation for Moscow, Russia
    data = [{"lon": longitude, "lat": latitude, "elevation": 200}]

    # Define the 3D scatterplot layer for the pinpoint location
    marker_layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position="[lon, lat, elevation]",
        get_radius=2000,  # Increase the marker size
        get_fill_color=[0, 255, 255, 150],  # Use RGBA format for transparency (0-255)
        pickable=True,
        auto_highlight=True,  # Enable hover highlighting
    )

    # Define the heatmap layer to indicate the location
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data,
        get_position="[lon, lat]",
        opacity=0.8,  # Adjust opacity as needed
        intensity=1,  # Adjust intensity as needed
        radius=2000,  # Adjust radius as needed
    )

    view_state = pdk.ViewState(
        longitude=longitude,
        latitude=latitude,
        zoom=12,  # Adjust zoom level for better visibility
        pitch=60,
        bearing=-30,
    )

    html_file = "C:/Users/1912a/Friday/functions/system/maps/3d_map.html"

    # Create the 3D map using Deck.gl with both marker and heatmap layers
    r = pdk.Deck(
        layers=[heatmap_layer, marker_layer],
        initial_view_state=view_state,
        tooltip={
            "text": "Elevation: {elevation} meters"
        },  # Add a tooltip for elevation
    )

    # Save the 3D map to the specified HTML file
    r.to_html(html_file)

    # Open the HTML file in a web browser
    webbrowser.open(html_file)


# Example usage:
create_three_d_map(longitude=37.6176, latitude=55.7558)  # Moscow coordinates
