<<<<<<< HEAD
import googlemaps, csv
from googlemaps.roads import snap_to_roads
from pathlib import Path
from peewee import * 
from setup import *
from tqdm import tqdm 

APIs = ['API_KEY_1', 'API_KEY_2']

def write(points): 
  # write to csv file 
  field_names = ('matched_lat', 'matched_lng', )
  with open('snapped.csv', 'w') as f:
    w = csv.DictWriter(f, fieldnames=field_names)
    
    for point in points:
      # renaming column name (key)
      point['location']['matched_lat'] = point['location'].pop('latitude')
      point['location']['matched_lng'] = point['location'].pop('longitude')
      w.writerow(point['location'])
      
def snap(coor, part):
  if part == 1:
    gmaps = googlemaps.Client(key=APIs[0])
  else:
    gmaps = googlemaps.Client(key=APIs[1])
  points = snap_to_roads(gmaps, coor) # points snapped to road
  write(points)

def split_insert(part):
  page = 0 
  coor = []
  if part == 1: # first half
    threshold = ((ProbePoint.select().count()/100)/2) 
  elif part == 2: # second half
    threshold = (ProbePoint.select().count()/100)
    page = ((ProbePoint.select().count()/100)/2)
  else:
    threshold = -1 # should never reach here
  
  while page != threshold:
    page += 1
    for point in tqdm(ProbePoint.select().paginate(page, 100)):
      coor.append((float(point.latitude), float(point.longitude)))
    snap(coor, part)
    del coor[:]

def main(): 
  # The logic goes by 1 page per 100 records. For example, page 1 would return 1-100, page 2 (101-200) etc. With 3000 or 
  # whichever the maximum row count is, it is divided by 100 to get the total amount of pages to iterate through and 
  # calling snap each time to check for the snapped coordinates.
  start_time = time.time()
  split_insert(1) # part 1 
  split_insert(2) # part 2

if __name__ == "__main__":
  main()
=======
from setup import (ProbePoint, LinkPoint)
from matching import belongs_to


def get_matched_probes(link):
    '''
    Given a link returns a list of nearby probes.

    :param link: a road link object
    :type link: setup.LinkPoint

    :return: a list of probes that are close to the given link
    :rtype: list[setup.ProbePoint]
    '''
    tolerance = 10
    (min_x, min_y) = (link.minX, link.minY)
    (max_x, max_y) = (link.maxX, link.maxY)

    # using raw query here because it's considerably faster
    query_text = '''
    SELECT * FROM probepoint
    WHERE x > ? - {tolerance} AND
          y > ? - {tolerance} AND
          x < ? + {tolerance} AND
          y < ? + {tolerance}
    '''.format(tolerance=tolerance)

    candidate_points = ProbePoint.raw(query_text, min_x, min_y, max_x, max_y)

    belongs_to_link = belongs_to(link)

    matched_probe_points = [p
                            for p in candidate_points.execute()
                            if belongs_to_link(p)]

    return matched_probe_points

def format_map_points(link, probes):
    '''
    For debugging purposes, output can be pasted directly into
    https://www.mapcustomizer.com/ bulk entry
    '''
    probes = '\n'.join(['{},{} <green>'.format(p.latitude, p.longitude)
                        for p in probes])

    link_points = '\n'.join(['{},{} <red>'.format(*link_point.split('/'))
                             for link_point in link.shapeInfo.split('|')])

    return '\n'.join([link_points, probes])


def main():
    for link in LinkPoint.select().limit(5):
        matched_probes = get_matched_probes(link)
        print('Matched {} probes'.format(len(matched_probes)))
        print('START'.center(40, '-'))
        print(format_map_points(link, matched_probes))
        print('END'.center(40, '-'))


if __name__ == '__main__':
    main()
>>>>>>> upstream/dev
