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

  # and this is where I break loose :(
  points = [result.json()['snappedPoints']
            for result in results]

  matched_latlons = [{p.get('originalIndex', -1): (p['location']['latitude'], p['location']['longitude'])
                     for p in ps} for ps in points]

  for (batch_idx, batch) in enumerate(in_chunks(probes, 100)):
    for (idx, probe) in enumerate(batch):
      latlon = matched_latlons[batch_idx].get(idx, None)
      probe.matchedLatitude = float(latlon[0]) if latlon else probe.latitude
      probe.matchedLongitude = float(latlon[1]) if latlon else probe.longitude

  return probes
