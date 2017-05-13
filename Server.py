from dbModels import session, Location
from sqlalchemy.exc import IntegrityError
from flask import Flask, request, abort
from math import radians, cos, sin, asin, sqrt
import json

app = Flask(__name__)

@app.route("/post_location", methods = ["POST"])
def postLocation():
    try:
        r = json.loads(request.data)
        req = Location(r['name'], r['lat'], r['lng'])
    except (ValueError, KeyError):
        abort(400)
    session.add(req)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        abort(409)
    return "Created", 201

def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    #convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    #haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

@app.route("/get_using_self", methods = ["GET"])
def getUsingSelf():
    r = request.args
    try:
        dist, lat, lng = (r['dist'], r['lat'], r['lng'])
    except KeyError:
        abort(400)
    dist, lat, lng = float(dist), float(lat), float(lng)
    locations = session.query(Location)
    filtered = {}
    for l in locations:
        if haversine(l.lat, l.lng, lat, lng) <= dist:
            record = {
                "lat": l.lat,
                "lng": l.lng,
            }
            filtered[l.name] = record
    return json.dumps(filtered)

@app.route("/get_using_postgres")
def getUsingPostgres():
    r = request.args
    try:
        dist, lat, lng = (r['dist'], r['lat'], r['lng'])
        #earthbox takes distance in meters
        dist = float(dist) * 1000
        lat = float(lat)
        lng = float(lng)
    except (KeyError, ValueError):
        abort(400)
    #possibility of sql injection is taken care during conversion to float
    #maybe create an index
    locations = session.execute(
        'select * from "locationsTable" \
        where earth_box(ll_to_earth({0}, {1}), {2}) @> \
        ll_to_earth(lat, lng)'.format(lat, lng, dist)
        )
    rtdata = {}
    for l in locations:
        rtdata[l.name] = {
            "lat": l.lat,
            "lng": l.lng,
        }
    return json.dumps(rtdata)


@app.route("/filldb", methods = ["GET"])
def fillDb():
    for lat in range(0, 90):
        print("Starting lat: " + str(lat))
        for lng in range(0, 180):
            name = "lat" + str(lat) + "lng" + str(lng)
            req = Location(name, lat, lng)
            session.add(req)
    print("Now committing.")
    session.commit()
    return "dumped"

app.run(host = "127.0.0.1", port = 5000)
