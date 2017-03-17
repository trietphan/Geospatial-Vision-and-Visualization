from dateutil import parser as datetime_parser
from pyproj import Geod
from math import atan
from statistics import mean

from utils import (first,
                   last,
                   add_items,
                   group_by,
                   pairwise,
                   dedup,
                   pairwise)

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

def compute_slope(p1, p2):
    rise = p1.altitude - p2.altitude
    run = get_distance((p1.latitude, p1.longitude), (p2.latitude, p2.longitude))
    try:
        return atan(rise / run)
    except ZeroDivisionError:
        return None

def get_updated_link_shape(link, probes, get_distance=get_distance):
    [ref_node_shape, *_] = link.shapeInfo.split('|')
    [ref_node_lat, ref_node_lon, slope] = ref_node_shape.split('/')

    ref_latlon = (float(ref_node_lat), float(ref_node_lon))

    get_distance_to_ref_node = lambda p: get_distance((p.matchedLatitude, p.matchedLongitude), ref_latlon)

    unique_probes = dedup(probes, get_distance_to_ref_node)
    sorted_by_distance = sorted(unique_probes,
                                key=get_distance_to_ref_node)

    slopes = [compute_slope(p1, p2)
              for (p1, p2) in pairwise(sorted_by_distance)]
    average_slope = mean([s for s in slopes if s])

    result = []
    for node in link.shapeInfo.split('|'):
        [lat, lon, slope] = node.split('/')
        result += ['{}/{}/{}'.format(lat, lon, slope if slope else average_slope)]

    return '|'.join(result)
