spatialite venues.sqlite "SELECT InitSpatialMetaData();"

spatialite venues.sqlite 'CREATE TABLE fsq_venues (
PK_UID INTEGER PRIMARY KEY AUTOINCREMENT,
fsq_id UNIQUE,
name TEXT,
category1 TEXT,
category2 TEXT,
category3 TEXT,
checkinsco INTEGER,
userscount INTEGER,
verified TEXT,
Geometry BLOB NOT NULL);'

spatialite venues.sqlite 'CREATE TABLE fsq_checkins (
PK_UID INTEGER PRIMARY KEY AUTOINCREMENT,
fsq_id TEXT,
timestamp TEXT,
request_id TEXT,
herenow INTEGER);'

#spatialite venues.sqlite "SELECT addGeometryColumn('fsq_venues', 'geom', 4326, 'POINT', 2);"

#INSERT INTO fsq_venues (fsq_id, geom, name, CategoryName, CategoryParents, Address, city, lat, lon, state, postalCode, checkinsCount, usersCount, verified)
#INSERT INTO fsq_requests (fsq_id, hereNow, request_id)