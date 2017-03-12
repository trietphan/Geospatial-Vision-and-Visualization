from math import (pi, tan, log, e)

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from setup import (ProbePoint, LinkPoint, MatchedPoints)
from utils import pairwise

def lat_lon_to_x_y(lat, lon):
    def ln(number):
        return log(number, e)

    def get_merc_number(lat):
        lat_radians = lat * pi / 180
        return ln(tan((pi / 4) + (lat_radians / 2)));

    (map_width, map_height) = (2000.0, 1000.0)

    x = (lon + 180) * (map_width / 360)
    y = (map_height / 2) - (map_width * get_merc_number(lon) / (2 * pi))

    return (x, y)

def shape_info_to_point(shape_info):
    [lat, lon, *_] = shape_info.split('/')
    (x, y) = lat_lon_to_x_y(float(lat), float(lon))

    return Point(x, y)

def is_near_line(line, point):
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
    link_points = [shape_info_to_point(p)
                   for p in link.shapeInfo.split('|')]

    return any(is_near_line(line, point)
               for line in pairwise(link_points))
