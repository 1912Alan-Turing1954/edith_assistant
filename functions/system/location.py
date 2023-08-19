from geopy.geocoders import Nominatim
import geocoder


# def get_location():
#     g = geocoder.ip("me")

#     if g.ok:
#         latitude = g.latlng[0]
#         longitude = g.latlng[1]
#         address = g.address
#         city = g.city
#         state = g.state
#         country = g.country
#         return {
#             "latitude": latitude,
#             "longitude": longitude,
#             "address": address,
#             "city": city,
#             "state": state,
#             "country": country,
#         }
#     else:
#         return None


def get_location():
    g = geocoder.ip("me")

    if g.ok:
        latitude = g.latlng[0]
        longitude = g.latlng[1]

        # Use Nominatim geocoder to get a detailed address
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        if location:
            address = location.raw.get("display_name", "")
            city = location.raw.get("address", {}).get("city", "")
            state = location.raw.get("address", {}).get("state", "")
            country = location.raw.get("address", {}).get("country", "")

            return {
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "city": city,
                "state": state,
                "country": country,
            }
        else:
            return None
    else:
        return None


location_data = get_location()


def get_location_description(response):
    description = response
    description = description.format(
        city=location_data["city"],
        state=location_data["state"],
        country=location_data["country"],
    )

    return description


def get_long_and_lati(response):
    description = response
    description = description.format(
        latitude=location_data["latitude"], longitude=location_data["longitude"]
    )

    return description


def get_address_description(response):
    description = response
    description = description.format(address=location_data["address"])
    return description
