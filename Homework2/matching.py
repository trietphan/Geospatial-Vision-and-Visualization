from math import (pi, tan, log, e)

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from setup import (ProbePoint, LinkPoint, MatchedPoints)
from utils import pairwise

def lat_lon_to_x_y(latlon):
    '''
    Given a tuple with (lat, lon) produce a tuple with (x, y)

    :param latlon: pair with latitude and longitude
    :type latlon: (float, float)

    :return: pair of x, y coordinates
    :rtype: (float, float)
    '''
    def ln(number):
        return log(number, e)

    def get_merc_number(lat):
        lat_radians = lat * pi / 180
        return ln(tan((pi / 4) + (lat_radians / 2)));

    (map_width, map_height) = (2000.0, 1000.0)
    (lat, lon) = latlon

    x = (lon + 180) * (map_width / 360)
    y = (map_height / 2) - (map_width * get_merc_number(lon) / (2 * pi))

    return (x, y)

def shape_info_unit_to_point(shape_info_unit):
    '''
    Given a string with shape info unit return a shapely Point object.

    :param shape_info_unit: string with shape info in "lat/lon/elevation?"
    :type shape_info_unit: str

    :return: a shapely Point with x,y coordinates
    :rtype: shapely.geometry.Point
    '''
    [lat, lon, *_] = shape_info_unit.split('/')
    (x, y) = lat_lon_to_x_y(float(lat), float(lon))

    return Point(x, y)

def is_near_line(line, point):
    '''
    Given a line and a point decide if point is near a line

    :param line: a pair of shapely points
    :type line: (shapely.geometry.Point, shapely.geometry.Point)
    :param point: a shapely point
    :type point: shapely.geometry.Point

    :return: is the point near the line
    :rtype: bool
    '''
    tolerance = 0.00001
    (p1, p2) = line
    ((x1, y1), (x2, y2)) = ((p1.x, p1.y), (p2.x, p2.y))

    a = [x1 - tolerance, y1 + tolerance]
    b = [x1 + tolerance, y1 - tolerance]
    c = [x2 - tolerance, y2 + tolerance]
    d = [x2 + tolerance, y2 - tolerance]

    bounds = Polygon([a, b, c, d])

    return point.within(bounds)

def belongs_to_link(link, point):
    link_points = [shape_info_unit_to_point(p)
                   for p in link.shapeInfo.split('|')]

    return any(is_near_line(line, point)
               for line in pairwise(link_points))
