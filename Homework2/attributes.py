from dateutil import parser as datetime_parser
from pyproj import Geod

from utils import (first, last, add_items, group_by, pairwise)

def get_distance(latlon1, latlon2):
    geod_inv = Geod(ellps='WGS84').inv
    (az12, az21, distance) = geod_inv(*latlon1, *latlon2)
    return distance

def find_directions(link, probes, get_distance=get_distance):
    by_sample_id = group_by('sampleID', probes)

    result = {}
    for (sample_id, probes) in by_sample_id:
        sorted_by_datetime = sorted(probes, key=lambda p: datetime_parser.parse(p.dateTime))

        if len(sorted_by_datetime) > 1:
            distance_from_first = find_distance_from_ref(link, first(sorted_by_datetime))
            distance_from_last = find_distance_from_ref(link, last(sorted_by_datetime))
            result[sample_id] = 'F' if distance_from_first < distance_from_last else 'T'
        else:
            result[sample_id] = '?'

    return result

def find_distance_from_ref(link, probe, get_distance=get_distance):
    [lat_ref, lon_ref, *_] = first(link.shapeInfo.split('|')).split('/')
    latlon_ref = (float(lat_ref), float(lon_ref))
    latlon_probe = (probe.latitude, probe.longitude)

    return get_distance(latlon_ref, latlon_probe)

def find_distance_from_link(probe, get_distance=get_distance):
    latlon_link = (probe.matchedLatitude, probe.matchedLongitude)
    latlon_probe = (probe.latitude, probe.longitude)

    return get_distance(latlon_link, latlon_probe)

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
