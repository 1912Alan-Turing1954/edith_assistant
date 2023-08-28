import pydeck as pdk
import webbrowser


def create_three_d_map(longitude, latitude, output_file="3d_map.html"):
    # Define your data with custom coordinates and elevation
    data = [{"lon": longitude, "lat": latitude, "elevation": 200}]

    # Define the 3D scatterplot layer for the pinpoint location
    marker_layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position="[lon, lat, elevation]",
        get_radius=200,  # Adjust marker size for better visibility
        get_fill_color=[0, 255, 255, 80],  # Adjust color and transparency (0-255)
        pickable=True,
        auto_highlight=True,
    )

    # Define the heatmap layer to indicate the location
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data,
        get_position="[lon, lat]",
        opacity=0.8,  # Adjust opacity as needed
        intensity=1,  # Reduce the intensity for a fading effect
        radius=2000,  # Adjust radius for heatmap
        color_range=[
            [0, 0, 0, 0],
            [0, 0, 255, 50],
            [0, 0, 255, 100],
            [0, 191, 255, 150],
            [0, 255, 255, 200],
            [255, 255, 0, 100],
            [255, 0, 0, 50],
        ],  # Customize heatmap color range for a fading effect
    )

    view_state = pdk.ViewState(
        longitude=longitude,
        latitude=latitude,
        zoom=15,  # Increase zoom level for better map quality
        pitch=60,
        bearing=-30,
    )

    # Create the 3D map using Deck.gl with both marker and heatmap layers
    deck = pdk.Deck(
        layers=[heatmap_layer, marker_layer],
        initial_view_state=view_state,
        tooltip={"text": "Elevation: {elevation} meters"},
    )

    # Save the 3D map to the specified HTML file
    deck.to_html(output_file)

    # Open the HTML file in a web browser
    webbrowser.open(output_file)
