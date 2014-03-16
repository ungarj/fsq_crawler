#!/usr/bin/env python 

import foursquare
import os

def main():
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
    	address = venue['location']['address']
    	lat = venue['location']['lat']
    	lon = venue['location']['lng']
    	state = venue['location']['state']
        postal_code = venue['location']['postalCode']
    	checkins_count = venue['stats']['checkinsCount']
    	users_count = venue['stats']['usersCount']
    	verified = venue['verified']
    	here_now = venue['hereNow']['count']

        print name
    	print address
    	print lat
    	print lon
    	print state
    	print postal_code
    	print checkins_count
    	print users_count
    	print verified
    	print here_now

    # TODO: get high level category
    #category_list = client.venues.categories()
    #for category in category_list:
    # 	print category['name']

    
if __name__ == "__main__":
    main()