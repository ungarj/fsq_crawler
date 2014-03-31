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

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--aoi", dest="aoi")
    parser.add_argument("--maxpoints", dest="maxpoints")
    parsed = parser.parse_args(args)
    maxpoints = parsed.maxpoints

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
    radius = max(len_a,len_b)/2
    
    # draw first hexagon --> results in 6+1 points
    points_start = []
    points_start.append(center)
    points_hexagon = draw_hexagon(center, radius)
    points_start.extend(points_hexagon)

    points_done = []
    points_todo = []

    for i in points_start:
        ## check_doubles

        ## check_within
        if Point(i).within(area):
            points_todo.append(i)
    ## true --> points todo

    points_total = []
    maxlevel = 2
    l=0
    points_thislevel = points_todo
    points_nextlevel=[]

    while l<maxlevel:
        radius = radius/2
        for k in points_thislevel:
            points_temp = draw_hexagon(Point(k), radius)
            for j in points_temp:
                if Point(j).within(area):
                    points_nextlevel.append(j)
        # TODO decide whether points go to points_done
        points_done.extend(points_thislevel)
        points_thislevel.extend(points_nextlevel)
        l=l+1

    m = MultiPoint(points_done)
    print len(points_done)
    print m
    

def draw_hexagon(center, radius):
    points = []
    point2 = Point((center.x+radius), center.y)
    line = LineString([(center.x, center.y), (point2.x, point2.y)])
    for i in [0,60,120,180,240,300]:
        templine = affinity.rotate(line, i, center)
        points.append(templine.coords[1])
    return points

def check_doubles(point, list):
    print "returns true or false"

def farthest_distance(point):
    print "returns distance of farthest result"

if __name__ == "__main__":
    main(sys.argv[1:])