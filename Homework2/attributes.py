from dateutil import parser as dateTimeParser
from pyproj import Geod

from utils import (first, last, add_items, group_by, pairwise)

def get_distance(latlon1, latlon2):
    geod_inv = Geod(ellps='WGS84').inv
    (az12, az21, distance) = geod_inv(*latlon1, *latlon2)
    return distance

def find_directions(link, probes, get_distance=get_distance):
    pass

def find_distance_from_ref(link, probe, get_distance=get_distance):
    pass

def find_distance_from_link(probe, get_distance=get_distance):
    pass

def create_matched_point(link, probe, get_direction):
    direction = get_direction(probe)
    distance_from_ref = find_distance_from_ref(link, probe)

    try:
        distance_from_link = find_distance_from_link(probe)
    except TypeError:
        distance_from_link = -1.0 # distance is unknown, point was not matched

    matched_point = {
        'sampleID': probe.sampleID,
        'dateTime': probe.dateTime,
        'sourceCode': probe.sourceCode,
        'latitude': probe.matchedLatitude if probe.matchedLatitude else probe.latitude, # default to
        'longitude': probe.matchedLongitude if probe.matchedLongitude else probe.longitude, # original values
        'altitude': probe.altitude,
        'speed': probe.speed,
        'heading': probe.heading,
        'linkPVID': link.linkPVID,
        'direction': direction,
        'distFromRef': distance_from_ref,
        'distFromLink': distance_from_link
    }

    return matched_point

def get_link_slope(link, probes, get_distance=get_distance):
    pass
