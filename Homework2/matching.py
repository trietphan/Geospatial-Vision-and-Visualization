from shapely.geometry import (Point, MultiPoint)
from shapely.geometry.polygon import Polygon

from pyproj import Proj

from utils import pairwise


def latlon_to_xy(latlon, projection=Proj(init='epsg:32618')):
    '''
    :param latlon: pair with latitude and longitude
    :type latlon: (float, float)
    :param projection: a function that will be used to convert (lat, lon) to (x, y)
    :type projection: function (float, float) -> (float, float)

    :return: pair of x, y coordinates
    :rtype: (float, float)
    '''
    (lat, lon) = latlon
    return projection(lat, lon)

def shape_info_unit_to_point(shape_info_unit):
    '''
    Given a string with shape info unit return a shapely Point object.

    :param shape_info_unit: string with shape info in "lat/lon/elevation?"
    :type shape_info_unit: str

    :return: a shapely Point with x,y coordinates
    :rtype: shapely.geometry.Point
    '''
    [lat, lon, *_] = shape_info_unit.split('/')
    latlon = (float(lat), float(lon))

    return Point(*latlon_to_xy(latlon))

def is_near_line(line, point, tolerance):
    '''
    Given a line and a point decide if point is near a line

    :param line: a pair of shapely points
    :type line: (shapely.geometry.Point, shapely.geometry.Point)
    :param point: a shapely point
    :type point: shapely.geometry.Point
    :param tolerance: half of width of the polygon drawn around the line
    :type tolerance: float

    :return: is the point near the line
    :rtype: bool
    '''
    (p1, p2) = line
    ((x1, y1), (x2, y2)) = ((p1.x, p1.y), (p2.x, p2.y))

    a = [x1 - tolerance, y1 + tolerance]
    b = [x1 + tolerance, y1 - tolerance]
    c = [x2 - tolerance, y2 + tolerance]
    d = [x2 + tolerance, y2 - tolerance]

    bounds = Polygon([a, b, c, d])

    return point.within(bounds)

def belongs_to(link):
    '''
    Given a link returns a function that determines wheter a point is close to a link

    :param link: a road link object
    :type link: setup.LinkPoint

    :return: function that takes in point and checks if it's close to link
    :rtype: function setup.ProbePoint -> bool
    '''
    tolerance = 15
    link_points = [shape_info_unit_to_point(p)
                   for p in link.shapeInfo.split('|')]

    def belongs_to_link(probe_point):
        '''
        :param probe_point: a probe point object
        :type probe_point: setup.ProbePoint

        :return:
        :rtype: bool
        '''
        probe_point_latlon = (float(probe_point.latitude), float(probe_point.longitude))
        point = Point(*latlon_to_xy(probe_point_latlon))
        return any(is_near_line(line, point, tolerance)
                   for line in pairwise(link_points))

    return belongs_to_link

def extract_shape_info_bounds(shape_info):
    '''
    Given shape info string return xy coordinate rectangle bounds for the shape

    :param shape_info: a shape info string with 'lat/lon/elevation?|lat/lon/elevation?|...' format
    :type shape_info: str

    :return: 2 pairs of xy coordinates for the bounding rectangle
    :rtype: ((float, float), (float, float))
    '''
    toks = (p.split('/') for p in shape_info.split('|'))
    latlons = ((float(ts[0]), float(ts[1])) for ts in toks)
    xys = [latlon_to_xy(latlon) for latlon in latlons]
    (min_x, min_y, max_x, max_y) = MultiPoint(xys).envelope.bounds

    return ((min_x, min_y), (max_x, max_y))
