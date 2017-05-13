from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import IntegrityError
from math import radians, cos, sin, asin, sqrt
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shreyansh@localhost/locations'
app.jinja_env.auto_reload = True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

dbctx = SQLAlchemy(app)
#maybe make index of all locations

class Location(dbctx.Model):
    __tablename__ = "locationsTable"
    name = dbctx.Column(dbctx.String(50), primary_key = True)
    lat = dbctx.Column(dbctx.Float(), nullable = False)
    lng = dbctx.Column(dbctx.Float(), nullable = False)

    def __init__(self, name, lat, lng):
        self.name = name[:50]
        self.lat = lat
        self.lng = lng

dbctx.create_all()

@app.route("/post_location", methods = ["POST"])
def postLocation():
    #make http errors more specific and helpful
    try:
        r = json.loads(request.data)
    except ValueError:
        abort(400)
    try:
        req = Location(r['name'], r['lat'], r['lng'])
    except KeyError:
        abort(400)
    dbctx.session.add(req)
    try:
        dbctx.session.commit()
    #use more specific exception and return status
    except Exception:
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
    locations = Location.query.all()
    filtered = {}
    for l in locations:
        if haversine(l.lat, l.lng, lat, lng) < dist:
            record = {
                "lat": l.lat,
                "lng": l.lng,
            }
            filtered[l.name] = record
    return json.dumps(filtered)

@app.route("/get_using_postgres")
def getUsingPostgres():
    r = request.args
"""try:
        dist, lat, lng = (r['dist'], r['lat'], r['lng'])
    except KeyError:
        abort(400)"""

@app.route("/filldb", methods = ["GET"])
def fillDb():
    for lat in range(0, 360):
        print("Starting lat: " + str(lat))
        for lng in range(0, 720):
            name = "lat" + str(lat) + "lng" + str(lng)
            req = Location(name, lat/4, lng/4)
            dbctx.session.add(req)
    print("Now committing.")
    dbctx.session.commit()
    return "dumped"

app.run(host = "127.0.0.1", port = 5000)
