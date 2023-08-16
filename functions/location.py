import geocoder


def get_location():
    g = geocoder.ip("me")

    if g.ok:
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        address = g.address
        city = g.city
        state = g.state
        country = g.country
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
    description = f"Your latitude is {location_data['latitude']} and your longitude is {location_data['longitude']}. "

    return description


def get_address_description(response):
    description = response
    description = description.format(address=location_data["address"])
    return description
