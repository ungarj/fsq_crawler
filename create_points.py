#!/usr/bin/env python 

# input: AOI, maximum number

import foursquare
import argparse
import ogr
import sys
import os
import json
from shapely.geometry import *
from shapely import affinity
import math
import time
import numpy
import hashlib
from sets import Set

ROUND = 4

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--aoi", dest="aoi")
    parser.add_argument("--maxpoints", dest="maxpoints")
    parsed = parser.parse_args(args)
    maxpoints = int(parsed.maxpoints)

    # read env variables
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    # Construct the client object
    client = foursquare.Foursquare(client_id, client_secret)
    
    # read input geojson
    with open(parsed.aoi, "r") as f:
        aoi_json = json.load(f)

    area = shape(aoi_json)
    bbox = area.bounds
    center = area.centroid
    # calculate first radius:
    ta = Point(bbox[0],center.y)
    tb = Point(center.x,bbox[1])
    len_a = center.distance(ta)
    len_b = center.distance(tb)
    radius = max(len_a,len_b)
    
    p=0
    points_thislevel=[] # points processed in current level
    points_thislevel.append(center) # initialized with center point
    points_nextlevel=[] # points to be processed in next loop: no doubles, within area and min distance
    points_done = [] # for every run, get appended by points_nextlevel
    start_point = True
    foursquare_request = 0
    double_hash = 0

    while len(points_done)<maxpoints:
        print "level: %s, points_thislevel: %s, points_done: %s, radius: %s" %(p, len(points_thislevel), len(points_done), radius)
        if p % 2 == 0:
            shift = True
        else:
            shift = False
        points_nextlevel = [] # reset to 0
        for k in points_thislevel:
            if (start_point==True): # special case for first loop
                points_nextlevel = draw_hexagon(Point(k), radius, shift)
                points_done = []
                points_done_hashes = Set()
                for i in points_thislevel:
                    hashstring = "%.4f %.4f" %(i.x,i.y)
                    h = hashstring
                    points_done_hashes.add(h)
                start_point = False
                h = ""
            else:
                points_nextlevel_temp = draw_hexagon(Point(k), radius, shift) # draw hexagons around points_thislevel
                for j in points_nextlevel_temp:
                    # create hash from j and compare with points_done_hashes
                    hashstring = "%.4f %.4f" %(j[0], j[1])
                    h = hashstring
                    if h in points_done_hashes:
                        double_hash = double_hash + 1
                        #print "duplicate %s %s" %(double_hash, hashstring)
                    else:
                        if Point(j).within(area):
                            request_lon = str(j[0])
                            request_lat = str(j[1])
                            print "making request"
                            #venue_list = client.venues.search(params={'ll' : request_lon+','+request_lat})
                            
                            points_done_hashes.add(h)
                            points_nextlevel.append(j)
                            foursquare_request = foursquare_request + 1
                    h=""

        for i in points_nextlevel:
            if Point(i).within(area):
                points_done.append(i)
        points_thislevel = points_nextlevel # add points for next run
        p=p+1
        radius = (radius/2)*math.sqrt(3)
        #time.sleep(1)
        if len(points_nextlevel)==0:
            break

    m = MultiPoint(points_done)
    #print foursquare_request
    #print "%s duplicates" %(double_hash)
    print m
    print len(points_done)
    #for i in points_done:
    #    print "%.4f %.4f" %(i[0], i[1])
    

def draw_hexagon(center, radius, shift):
    points = []
    point2 = Point((center.x+radius), center.y)
    line = LineString([(center.x, center.y), (point2.x, point2.y)])
    degrees = numpy.array([0,60,120,180,240,300])
    if shift==True:
        degrees = degrees + 30
    for i in degrees:
        templine = affinity.rotate(line, i, center)
        points.append(templine.coords[1])
    points.append([center.x, center.y])
    return points

def check_unique(point, pointlist):
    unique = True
    for i in pointlist:
        if Point(point).almost_equals(Point(i),4):
            unique = False
    return unique


def farthest_distance(point):
    print "returns distance of farthest result"

if __name__ == "__main__":
    main(sys.argv[1:])