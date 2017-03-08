import csv, json
from peewee import * 
from datetime import datetime
from pathlib import Path
from tqdm import tqdm # optional 

db = SqliteDatabase('probe.db')

def setup(): 
  class ProbeBase(Model): 
    class Meta: 
      database = db

  class ProbePoint(ProbeBase):
    sampleID = IntegerField() # ID is NOT unique
    dateTime = DateTimeField()
    sourceCode = IntegerField()
    latitude = DecimalField()
    longitude = DecimalField()
    altitude = IntegerField()
    speed = IntegerField() # stored in KPH 
    heading = IntegerField() # degrees 

  db.connect() # explicitness for safety
  db.create_tables([ProbePoint], safe=True)
  f = open('probe.csv', 'rU')
  reader = csv.DictReader(f, fieldnames=("sampleID", "dateTime", "sourceCode", "latitude", "longitude", "altitude", "speed", "heading"))
  
  # writing to database 
  for point in tqdm(list(reader)): 
    ProbePoint.create(sampleID=point['sampleID'], dateTime=point['dateTime'], sourceCode=point['sourceCode'], latitude=point['latitude'], longitude=point['longitude'], altitude=point['altitude'], speed=point['speed'], heading=point['heading']).save()
  db.close()

def main(): 
  file = Path('probe.db')
  if not file.is_file():
    print("Setting up database...")
    setup()
    print("Database created.")
  else:
    print("Database Found!")
    
if __name__ == "__main__":
  main()