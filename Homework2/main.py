import googlemaps, json
from googlemaps.roads import snap_to_roads
from pathlib import Path
from peewee import * 
from setup import (ProbeBase, ProbePoint)
from tqdm import tqdm 
import time

gmaps = googlemaps.Client(key="AIzaSyCrMmLtpBaKBiAPrECOUwHbXIbMvK3IABc")
def write(points): 
  file = Path('data.json')
  if not file.is_file(): # first insert
    with open('data.json', 'w') as f: 
      json.dump(points, f, sort_keys=True, indent=2)
  else: # append
    with open('data.json') as f:
      data = json.load(f)
    data.append(points)
    with open('data.json', 'w') as f:
      json.dump(data, f, sort_keys=True, indent=2)

def snap(coor):
  points = snap_to_roads(gmaps, coor) # points snapped to road
  write(points)

def main(): 
  # The logic goes by 1 page per 100 records. For example, page 1 would return 1-100, page 2 (101-200) etc. With 3000 or 
  # whichever the maximum row count is, it is divided by 100 to get the total amount of pages to iterate through and 
  # calling snap each time to check for the snapped coordinates.
  start_time = time.time()
  page = 0
  coor = []
  while page != (ProbePoint.select().count()/100): 
    page += 1
    for point in tqdm(ProbePoint.select().paginate(page, 100)):
      coor.append((float(point.latitude), float(point.longitude)))
    snap(coor)
    del coor[:]
  print("time used: {}s".format(time.time() - start_time)) # roughly 4 seconds for 3000 points 

if __name__ == "__main__":
  main()