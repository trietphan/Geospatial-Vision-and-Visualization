import os

def create_url(center, size=20):
    '''
    Create a url that can be used to retrieve the image for a given center
    :param center: (lat, lon) pair of the center of the image
    :type center: (float, float)

    :return:
    :rtype: str
    '''
    BASE = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial'

    location_extension = ','.join(map(str, center))
    size_extension = str(size)

    return '/'.join([BASE, location_extension, size_extension])

def create_request_params():
    API_KEY = os.environ['API_KEY']
    MAP_SIZE = (512, 572)
    return {
        'mapSize': ','.join(map(str, MAP_SIZE)),
        'key': API_KEY
    }
