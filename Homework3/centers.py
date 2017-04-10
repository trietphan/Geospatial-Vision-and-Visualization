from math import (atan, exp, pi, sin, radians, log)
from itertools import product

def clip(n, min_value, max_value):
    '''
    Clips a number to the specified minimum and maximum values.

    :param n: the number to clip
    :type n: float
    :param min_value: minimum allowable value
    :type min_value: float
    :param max_value: maximum allowable valuea
    :type max_value: float

    :rtype: float
    '''
    return min(max(n, min_value), max_value)

def get_map_size(detail_level):
    '''
    :param detail_level: level of detail (1..23)
    :type detail_level: int

    :rtype: int
    '''
    return 256 << detail_level

def pixel_to_latlon(point, detail_level=20):
    '''
    :param point: (x, y) pair of coordinates for a point in pixels
    :type point: (int, int)
    :param detail_level: level of detail (1..23)
    :type detail_level: int

    :return: pair of (lat, lon)
    :rtype: (float, float)
    '''
    (pixel_x, pixel_y) = point
    map_size = get_map_size(detail_level)
    x = (clip(float(pixel_x), 0, map_size - 1) / map_size) - 0.5
    y = 0.5 - (clip(float(pixel_y), 0, map_size - 1) / map_size)

    lat = 90 - 360 * atan(exp(-y * 2 * pi)) / pi
    lon = 360 * x

    return (lat, lon)

def latlon_to_pixel(latlon, detail_level=20):
    '''
    :param latlon: (lat, lon) pair of coordinates
    :type latlon: (float, float)
    :param detail_level: level of detail (1..23)
    :type detail_level: int

    :return: pair of (x, y)
    :rtype: (int, int)
    '''
    (MIN_LAT, MIN_LON) = (-85.05112878, -180)
    (MAX_LAT, MAX_LON) = (85.05112878, 180)

    (lat, lon) = (clip(latlon[0], MIN_LAT, MAX_LAT), clip(latlon[1], MIN_LON, MAX_LON))
    map_size = get_map_size(detail_level)

    x = (lon + 180) / 360
    y = 0.5 - log((1 + sin(radians(lat))) / (1 - sin(radians(lat)))) / (4 * pi)

    pixel_x = int(clip(x * map_size + 0.5, 0, map_size - 1))
    pixel_y = int(clip(y * map_size + 0.5, 0, map_size - 1))

    return (pixel_x, pixel_y)

def find_centers(latlon1, latlon2, size=(512, 512)):
    '''
    Find all of the possible centers given a pair of (lat, lon) coordinates
    :param latlon1: southwest coordinate pair (lat, lon)
    :type latlon1: (float, float)
    :param latlon2: northeast coordinate pair (lat, lon)
    :type latlon2: (float, float)

    :return: list of (lat, lon) centers for pictures and number of columns
    :rtype: ([(float, float)], int)
    '''
    (pixel_x1, pixel_y1) = latlon_to_pixel(latlon1)
    (pixel_x2, pixel_y2) = latlon_to_pixel(latlon2)

    xs = range(pixel_x1, pixel_x2 + 1, size[0])
    ys = range(pixel_y1, pixel_y2 + 1, -size[1])

    num_columns = len(ys)
    centers = [pixel_to_latlon(p)
               for p in product(xs, ys)]

    return (centers, num_columns)
