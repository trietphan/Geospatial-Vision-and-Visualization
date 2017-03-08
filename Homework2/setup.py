import csv
from peewee import * 
from pathlib import Path
from tqdm import tqdm # optional - remember to install tqdm using pip/pip3 

db = SqliteDatabase('probe.db')

class ProbeBase(Model):
  class Meta: 
    database = db

class ProbePoint(ProbeBase):
  sampleID    = BigIntegerField() # ID is NOT unique
  dateTime    = DateTimeField()
  sourceCode  = IntegerField()
  latitude    = DecimalField()
  longitude   = DecimalField()
  altitude    = IntegerField()
  speed       = IntegerField() # stored in KPH 
  heading     = IntegerField() # degrees 

class LinkPoint(ProbeBase):
  linkPVID          = BigIntegerField()
  refNodeID         = BigIntegerField()
  nrefNodeID        = BigIntegerField
  length            = DecimalField()
  functionalClass   = IntegerField()
  directionOfTravel = CharField()
  speedCategory     = IntegerField()
  fromRefSpeedLimit = IntegerField()
  toRefSpeedLimit   = IntegerField()
  fromRefNumLanes   = IntegerField()
  toRefNumLanes     = IntegerField()
  multiDigitized    = BooleanField()
  urban             = BooleanField()
  timeZone          = DecimalField()
  shapeInfo         = TextField() # array
  curvatureInfo     = TextField() # array
  slopeInfo         = TextField() # array 

class MatchedPoints(ProbeBase):
  sampleID      = IntegerField() # ID is NOT unique
  dateTime      = DateTimeField()
  sourceCode    = IntegerField()
  latitude      = DecimalField()
  longitude     = DecimalField()
  altitude      = IntegerField()
  speed         = IntegerField() # stored in KPH 
  heading       = IntegerField() # degrees 
  linkPVID      = BigIntegerField()
  direction     = CharField()
  distFromRef   = IntegerField()
  distFromLink  = IntegerField()

def db_connect_handler(): 
  db.connect() # explicitness for safety

def db_close_handler():
  db.close()

def setup(db): 
  db_connect_handler()
  db.create_tables([ProbePoint, LinkPoint, MatchedPoints], safe=True)
  
  # Probe Data 
  f = open('probe.csv', 'rU')
  ProbeRead = csv.DictReader(f, fieldnames=("sampleID", "dateTime", "sourceCode", "latitude", "longitude", "altitude", "speed", "heading"))
  
  # Link Data
  f = open('link.csv', 'rU')
  LinkRead = csv.DictReader(f, fieldnames=("linkPVID", "refNodeID", "nrefNodeID", "length", "functionalClass", "directionOfTravel", "speedCategory", "fromRefSpeedLimit", "toRefSpeedLimit", "fromRefNumLanes", "toRefNumLanes", "multiDigitized", "urban", "timeZone", "shapeInfo", "curvatureInfo", "slopeInfo"))
  
  # Writing to database
  with db.atomic():
    for point in tqdm(list(ProbeRead)[:3000]): # remove [] to insert all rows
      ProbePoint.create(sampleID=point['sampleID'], dateTime=point['dateTime'], sourceCode=point['sourceCode'], latitude=point['latitude'], longitude=point['longitude'], altitude=point['altitude'], speed=point['speed'], heading=point['heading']).save()
    
    for point in tqdm(list(LinkRead)[:3000]):
      LinkPoint.create(linkPVID=point['linkPVID'], refNodeID=point['refNodeID'], nrefNodeID=point['nrefNodeID'], length=point['length'], functionalClass=point['functionalClass'], directionOfTravel=point['directionOfTravel'], speedCategory=point['speedCategory'], fromRefSpeedLimit=point['fromRefSpeedLimit'], toRefSpeedLimit=point['toRefSpeedLimit'], fromRefNumLanes=point['fromRefNumLanes'], toRefNumLanes=point['toRefNumLanes'], multiDigitized=point['multiDigitized'], urban=point['urban'], timeZone=point['timeZone'], shapeInfo=point['shapeInfo'], curvatureInfo=point['curvatureInfo'], slopeInfo=point['slopeInfo']).save()
  db_close_handler()

def main(): 
  file = Path('probe.db')
  if not file.is_file():
    print("Setting up database...")
    setup(db)
    print("Database created.")
  else:
    print("Database found!")

if __name__ == "__main__":
  main()