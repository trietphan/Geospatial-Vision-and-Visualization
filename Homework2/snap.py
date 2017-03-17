import grequests
import os

from setup import ProbePoint
from utils import (in_chunks, flatten)


def create_params(probes):
  result = []
  for batch in in_chunks(probes, 100):
    path = '|'.join(['{},{}'.format(p.latitude, p.longitude)
                     for p in batch])
    interpolate = True

    api_key = os.environ['API_KEY'] # will raise KeyError if not found

    request_parameters = {
      'path': path,
      'interpolate': interpolate,
      'key': api_key
    }

    result += [request_parameters]

  return result

def match_probes(probes):
  url = 'https://roads.googleapis.com/v1/snapToRoads'
  request_parameters = create_params(probes)
  results = grequests.map(grequests.get(url, params=params)
                          for params in request_parameters)

  points = flatten([result.json()['snappedPoints']
                    for result in results])

  matched_latlons = [(p['location']['latitude'], p['location']['longitude'])
                     for p in points]

  matched_probes = []
  for (probe, matched_latlon) in zip(probes, matched_latlons):
    probe.matchedLatitude = matched_latlon[0]
    probe.matchedLongitude = matched_latlon[1]

  return probes
