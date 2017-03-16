from setup import (ProbePoint, LinkPoint, MatchedPoint)
from matching import belongs_to
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime

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


#Given map matched probe points identify the direction of the probe within a link (look at first and last points within a link, and compare the time recorded, shouldn't be too bad)
#direction	is the direction the vehicle was travelling on thelink (F = from ref node, T = towards ref node).
#distFromRef	is the distance from the reference node to the map-matched probe point location on the link in decimal meters.
#distFromLink	is the perpendicular distance from the map-matched probe point location on the link to the probe point in decimal meters.

def calcOtherInfo(link, probes):
    [ref_node, *_] = link.shapeInfo.split("|", 1)
    (ref_lat, ref_lon, ref_ele) = ref_node.split("/")
    ref_lat = radians(float(ref_lat))
    ref_lon = radians(float(ref_lon))
    R = 6373.0                  # approximate radius of earth in km
    sIDinfo = []                # collection of sampleIDs, their dateTimes, and distFromRefs 
    savedsIDD = []              # saved sampleID and Direction pairs
    direction = '?'
    matched_points = []
    #Tools to keep track of the various calculations here
    #probeidx = 0
    #directions = []
    #distFromRefs = []
    #distFromLinks = []
    
    for p in probes:
        #Get the distance from the link's refnode to the point
        p_lat = radians(p.latitude)
        p_lon = radians(p.longitude)
        dist_lon = p_lon - ref_lon
        dist_lat = p_lat - ref_lat
        a = sin(dist_lat / 2)**2 + cos(p_lat) * cos(ref_lat) * sin(dist_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))        
        distFromRef = R * c
        #Distance formula based off of http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

        #distFromRefs[probeidx] = distance
        #probeidx += 1

        #Get the direction
        #direction is same for all points from a given sampleID

        idx = None
        idx = savedsIDD.index(p.sampleID) if p.sampleID in savedsIDD else None
        if idx is not None:
            #first case: we already have the direction stored for this sampleID in the savedSIDD list
            #directions[probeidx] = sIDD[idx + 1]
            direction = savedsIDD[idx + 1]
            print('case 1')
        else:
            #all other cases: we have seen this sampleID only once before or never
            idx = None
            #find out if we've seen this sample ID before
            for s in sIDinfo:
                if p.sampleID in s:
                    idx = sIDinfo.index(s)
                    break
            if idx is None:
                #case 2: we have not seen this sampleID before, not enough information to get a direction yet so we store this point's distFromRef and dateTime
                sIDinfo.append([p.sampleID, distFromRef, p.dateTime])
                print('case 2')
            else:
                #case 3: we have seen this sampleID before, so we calculate the direction based off the previously stored point's information
                if sIDinfo[idx][1] < distFromRef:
                    if datetime(sIDinfo[idx][2]) < datetime(p.dateTime):
                        direction = 'F'
                        print('case 3a')
                    else: 
                        direction = 'T'
                        print('case 3b')
                else:
                    if datetime(sIDinfo[idx][2]) < datetime(p.dateTime):
                        direction = 'T'
                        print('case 3c')
                    else: 
                        direction = 'F'
                        print('case 3d')
                #now that we know the direction, we don't need to save this sampleIDs info anymore, we can just add it to savedSIDDs
                savedsIDD.append(p.sampleID)
                savedsIDD.append(direction)
                del sIDinfo[idx]
        #end get direction

        #calculate distFromLink

        #add point and point data to matched_points list of dictionaries
        matched_points = {'sampleID': p.sampleID,'dateTime':p.dateTime,'sourceCode':p.sourceCode,'latitude':p.latitude, 'longitude':p.longitude, 'altitude':p.altitude, 'speed':p.speed, 'heading':p.heading, 'linkPVID':link.linkPVID, 'direction':direction, 'distFromRef':distFromRef, 'distFromLink':None}
        return matched_points



def main():
    final_matched_probes = []
    i = 0
    for link in LinkPoint.select().limit(1):
        matched_probes = get_matched_probes(link)        
        #print(matched_probes[0].latitude)
        print('Matched {} probes'.format(len(matched_probes)))
        print('START'.center(40, '-'))
        print(format_map_points(link, matched_probes))
        print('END'.center(40, '-'))
        for p in matched_probes:
            final_matched_probes.append(calcOtherInfo(link, matched_probes))
            print('distFromRef: ', final_matched_probes[i]['distFromRef'])
            print('direction: ', final_matched_probes[i]['direction'])
            print('distFromLink: ',final_matched_probes[i]['distFromLink'])
            i += 1


if __name__ == '__main__':
    main()
