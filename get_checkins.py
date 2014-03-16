#!/usr/bin/env python 

import foursquare
import os
from pyspatialite import dbapi2 as db
import sys
import argparse
import json

def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("--coords", dest="coords")
    parsed = parser.parse_args(args)
    
    # creating/connecting to db
    conn = db.connect('venues.sqlite')
    # creating a Cursor
    cur = conn.cursor()

    # read env variables
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    # Construct the client object
    client = foursquare.Foursquare(client_id, client_secret)

    with open(parsed.coords, "r") as f:
        coords = json.load(f)

    for point in coords['request_points']:
        request_lat = point['lat']
        request_lon = point['lon']

        print "checking point %s %s" %(request_lat, request_lon)

        # search for venues
        venue_list = client.venues.search(params={'ll' : request_lon+','+request_lat, })    

        for venue in venue_list['venues']:
            fsq_id = venue['id']
            name = venue['name']
            #category_name venue['categories']
            #category_parents venue['categories']
            #address = venue['location']['address']
            lat = venue['location']['lat']
            lon = venue['location']['lng']
            #state = venue['location']['state']
            #postal_code = venue['location']['postalCode']
            checkins_count = venue['stats']['checkinsCount']
            users_count = venue['stats']['usersCount']
            verified = venue['verified']
            here_now = venue['hereNow']['count']    

            # TODO: get high level category
            #category_list = client.venues.categories()
            #for category in category_list:
            #     print category['name']    

            try:
                insert_venue = 'INSERT OR IGNORE INTO fsq_venues (fsq_id, name, Geometry) VALUES ("%s","%s", GeomFromText("POINT(%s %s)"));' %(fsq_id, name, lon, lat)
                #print insert_venue
                cur.execute(insert_venue)
                conn.commit()
            except:
            	print "insert error"


if __name__ == "__main__":
    main(sys.argv[1:])