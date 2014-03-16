spatialite venues.sqlite "SELECT InitSpatialMetaData();"

spatialite venues.sqlite "CREATE TABLE fsq_venues
( PKUID INTEGER PRIMARY KEY AUTOINCREMENT ,
  fsq_id           TEXT,
  name             TEXT,
  CategoryName     TEXT,
  CategoryParents  TEXT,
  Address          TEXT,
  city             TEXT,
  lat             FLOAT,
  lon             FLOAT,
  state            TEXT,
  postalCode        INT,
  checkinsCount     INT,
  usersCount        int,
  verified         TEXT
);"

spatialite venues.sqlite "SELECT addGeometryColumn('fsq_venues', 'geom', 4326, 'MULTILINESTRING', 2);"

#INSERT INTO fsq_venues (fsq_id, geom, name, CategoryName, CategoryParents, Address, city, lat, lon, state, postalCode, checkinsCount, usersCount, verified)
#INSERT INTO fsq_requests (fsq_id, hereNow, request_id)