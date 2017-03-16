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