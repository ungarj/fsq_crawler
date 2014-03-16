#!/usr/bin/env python 

import foursquare
import os
from pyspatialite import dbapi2 as db


def main():

    # creating/connecting the test_db
    conn = db.connect('venues.sqlite')
    # creating a Cursor
    cur = conn.cursor()

    # read env variables
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    # Construct the client object
    client = foursquare.Foursquare(client_id, client_secret)

    # search for venues
    venue_list = client.venues.search(params={'ll' : '48.20626,16.34939'})

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

        #print name
    	#print lat
    	#print lon
    	#print checkins_count
    	#print users_count
    	#print verified
    	#print here_now

        insert_venue = 'INSERT INTO fsq_venues (fsq_id, name, Geometry) VALUES ("%s","%s", GeomFromText("POINT(%s %s)"));' %(fsq_id, name, lon, lat)
        print insert_venue
        cur.execute(insert_venue)
        conn.commit()

    # TODO: get high level category
    #category_list = client.venues.categories()
    #for category in category_list:
    # 	print category['name']

    # testing library versions
    #rs = cur.execute('SELECT sqlite_version(), spatialite_version()')
    #for row in rs:
    #    msg = "> SQLite v%s Spatialite v%s" % (row[0], row[1])
    #    print msg
    
if __name__ == "__main__":
    main()