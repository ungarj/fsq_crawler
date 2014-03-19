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
    
    # creating/connecting to spatialite file
    conn = db.connect('venues.sqlite')
    # creating a Cursor
    cur = conn.cursor()

    # read env variables
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    # Construct the client object
    client = foursquare.Foursquare(client_id, client_secret)

    category_tree = client.venues.categories()['categories']

    with open(parsed.coords, "r") as f:
        coords = json.load(f)

    for point in coords['request_points']:
        request_lat = point['lat']
        request_lon = point['lon']

        print "checking point %s %s" %(request_lat, request_lon)

        # generate timestamp and request_id
        request_id = "2014-03-22"
        timestamp = "2014-03-22"

        # search for venues
        venue_list = client.venues.search(params={'ll' : request_lon+','+request_lat}) 

        print "%s venues found" %(len(venue_list['venues']))

        for venue in venue_list['venues']:

            # get primary category
            categories = venue['categories']
            for category in categories:
                if category['primary']==True:
                    category_id = category['id']
                    category_name = category['name']

            # fill category hierachies
            venue_cat1 = "NULL"
            venue_cat2 = "NULL"
            venue_cat3 = "NULL"
            for category1 in category_tree:
                if category1['id'] == category_id:
                    venue_cat1 = category1['name']
                for category2 in category1['categories']:
                    if category2['id'] == category_id:
                        venue_cat1 = category1['name']
                        venue_cat2 = category2['name']
                    for category3 in category2['categories']:
                        if category3['id'] == category_id:
                            venue_cat1 = category1['name']
                            venue_cat2 = category2['name']
                            venue_cat3 = category3['name']

            fsq_id = venue['id']
            name = venue['name']
            lat = venue['location']['lat']
            lon = venue['location']['lng']
            checkins_count = venue['stats']['checkinsCount']
            users_count = venue['stats']['usersCount']
            verified = venue['verified']
            here_now = venue['hereNow']['count']    

            # TODO: get high level category
            #category_list = client.venues.categories()
            #for category in category_list:
            #     print category['name']

            #print "%s: %s, %s, %s" %(name, venue_cat1, venue_cat2, venue_cat3)


            # write data to spatialite file
            try:
                insert_venue = 'INSERT OR IGNORE INTO fsq_venues (fsq_id, name, category1, category2, category3, checkinsco, userscount, verified, Geometry) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s", GeomFromText("POINT(%s %s)"));' %(fsq_id, name, venue_cat1, venue_cat2, venue_cat3, checkins_count, users_count, verified, lon, lat)
                cur.execute(insert_venue)
                if here_now > 0:
                    insert_checkins = 'INSERT OR IGNORE INTO fsq_checkins (fsq_id, timestamp, request_id, herenow) VALUES ("%s","%s","%s","%s");' %(fsq_id, timestamp, request_id, here_now)
                    cur.execute(insert_checkins)
             
                conn.commit()
            except:
            	print "insert error"

            #print "\n"
    

if __name__ == "__main__":
    main(sys.argv[1:])