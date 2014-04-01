#!/usr/bin/env python 

# input: AOI, maximum number

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

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--aoi", dest="aoi")
    parser.add_argument("--maxpoints", dest="maxpoints")
    parsed = parser.parse_args(args)
    maxpoints = int(parsed.maxpoints)

    # read env variables
    #client_id = os.environ['CLIENT_ID']
    #client_secret = os.environ['CLIENT_SECRET']

    # Construct the client object
    #client = foursquare.Foursquare(client_id, client_secret)
    # foursquare zeugs muss global bleiben
    
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

    while len(points_done)<maxpoints:
        print "level: %s, points_nextlevel: %s, points_done: %s, radius: %s" %(p, len(points_nextlevel), len(points_done), radius)
        if p % 2 == 0:
            shift = True
        else:
            shift = False
        print shift
        points_nextlevel_all = []
        points_nextlevel = [] # reset to 0
        for k in points_thislevel:
            if (start_point==True): # special case for first loop
                points_nextlevel = draw_hexagon(Point(k), radius, shift)
                points_done = points_thislevel
                start_point = False
            else:
                points_nextlevel_temp = draw_hexagon(Point(k), radius, shift) # draw hexagons around points_thislevel
                for j in points_nextlevel_temp:
                    # create hash from j and compare with points_nextlevel_all
                    # if new, add to points_nextlevel
                    foursquare_request = foursquare_request + 1
                    points_nextlevel.append(j)
            points_nextlevel_all.extend(points_nextlevel) # current snapshot for double check
        for i in points_nextlevel:
            if Point(i).within(area):
                points_done.append(i)
        points_thislevel = points_nextlevel # add points for next run
        p=p+1
        radius = (radius/2)*math.sqrt(3)
        #time.sleep(1)

    m = MultiPoint(points_done)
    print foursquare_request
    print m
    

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
    points.append(center)
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