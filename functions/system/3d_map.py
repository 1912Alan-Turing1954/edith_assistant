import pydeck as pdk
import webbrowser


def create_3d_map(longitude, latitude):
    # Define your data with custom coordinates and elevation for Moscow, Russia
    data = [{"lon": longitude, "lat": latitude, "elevation": 200}]

    # Define the 3D scatterplot layer and other visualization options
    layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position="[lon, lat, elevation]",
        get_radius=1000,
        get_fill_color=[0, 255, 255],
        pickable=True,
    )

    view_state = pdk.ViewState(
        longitude=longitude,
        latitude=latitude,
        zoom=6,
        pitch=60,
        bearing=-30,
    )

    html_file = "C:/Users/1912a/Friday/functions/system/maps/3d_map.html"

    # Create the 3D map using Deck.gl
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)

    # Save the 3D map to the specified HTML file
    r.to_html(html_file)

    # Open the HTML file in a web browser
    webbrowser.open(html_file)
