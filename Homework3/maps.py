import os
import grequests

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

def get_images(centers):
    '''
    Given a list of centers get a list of images
    :param centers: (lat, lon) list of pairs
    :type center: iterable[(float, float)]

    :return: generator with images that correspond to given centers
    :rtype: generator[bytes]
    '''
    urls = (create_url(c) for c in centers)
    params = create_request_params()

    results = grequests.map(grequests.get(url, params=params)
                            for url in urls)

    images = (r.content for r in results)

    return images
