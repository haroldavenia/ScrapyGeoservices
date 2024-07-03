import random


def _get_random_coord(num_points):
    coordinates = []
    for _ in range(num_points):
        latitude = random.uniform(24.396308, 31.000965)
        longitude = random.uniform(-87.634643, -79.974307)
        coordinates.append({'x': longitude, 'y': latitude})
    return _generate_additional_coordinates(coordinates)


def _generate_additional_coordinates(coords):
    add_coords = []
    numbers = []
    for _ in range(20):
        number = random.randint(0, 99)
        numbers.append(number)

    for number in numbers:
        coord = coords[number]
        for _ in range(random.randint(2, 5)):
            additional_longitude = coord['x'] + random.uniform(-0.140, 0.140)
            additional_latitude = coord['y'] + random.uniform(-0.140, 0.140)
            add_coords.append({'x': additional_longitude, 'y': additional_latitude})

    return coords + add_coords


def demo_friends_loc(loc):
    locations = _get_random_coord(100)
    if len(locations) > 1:
        return loc.cluster_dense_centroid(locations)
    else:
        return locations[0]


def text_tweet_loc():
    text = u"On February 3, a horrifying railroad accident took place. " \
           u"A Norfolk Southern freight train derailed in East Palestine, Ohio. " \
           u"You might've seen images of the flames, but you probably haven't heard " \
           u"that unions were trying to prevent this exact accident."
    return text
