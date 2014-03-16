spatialite venues.sqlite "SELECT InitSpatialMetaData();"

spatialite venues.sqlite 'CREATE TABLE fsq_venues (
PK_UID INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp TEXT,
request_id TEXT,
herenow INTEGER,
fsq_id TEXT,
id INTEGER,
name TEXT,
categoryna TEXT,
categorypa TEXT,
address TEXT,
city TEXT,
lat DOUBLE,
lon DOUBLE,
state TEXT,
postalcode TEXT,
checkinsco INTEGER,
userscount INTEGER,
verified TEXT,
Geometry BLOB NOT NULL);'

#spatialite venues.sqlite "SELECT addGeometryColumn('fsq_venues', 'geom', 4326, 'POINT', 2);"

#INSERT INTO fsq_venues (fsq_id, geom, name, CategoryName, CategoryParents, Address, city, lat, lon, state, postalCode, checkinsCount, usersCount, verified)
#INSERT INTO fsq_requests (fsq_id, hereNow, request_id)