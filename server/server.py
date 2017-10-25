#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from datetime import datetime
import calendar




import json
import numpy as np

def get_timestamps(evts):
	return [c['timestamp'] for c in evts['content']]


def get_bucket(dt):
	return dt.weekday() * 24 + dt.hour


from collections import namedtuple
AllData = namedtuple('AllData', ['spots', 'trends', 'total'])

import pickle

def load_data():
	with open('all_data.p', 'rb') as f:
		all_pickled = f.read()
		return pickle.loads(all_pickled)

all_data = load_data()

def get_coords(data):
	coords = []
	for l in data["content"]:
	    coord = [list(reversed([float(c) for c in pt.split(':')])) for pt in l["coordinates"].split(',')]
	    coords.append((l['locationUid'], coord))
	return coords


def tuple_to_hex(color_tuple):
    print(color_tuple)
    return '#%02x%02x%02x' % tuple(color_tuple)


def layer_for_spot(name, coords):
    try:
        idx = all_data.spots.index(name)
    except:
        idx = None

    dt = datetime(2017, 10, 28, 20, 47, 0) 
    bucket = get_bucket(dt)

#start_ts = get_timestamp(datetime(2017, 10, 17, 23, 47, 0))
#end_ts = get_timestamp(datetime(2017, 10, 24, 23, 47, 0))

    unavail = (0, 0, 200)
    errc = (200, 200, 200)
    unavail = errc

    if idx is not None:
        act = all_data.trends[bucket][idx]
        tot = all_data.total[idx]
        print('act,tot', act, tot)
        pct = act / float(tot)
        # make it look greener
        # pct *= 4

        full = (255, 0, 0)
        free = (0, 255, 0)

        try:
            c = [int(freei * pct + fulli * (1 - pct)) for freei, fulli in zip(free, full)]
        except:
            c = errc
    else:
        c = unavail

    chex = tuple_to_hex(c)

    return {
        'id': name,
        'type': 'fill',
        'source': {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [coords]
                }
            }
        },
        'layout': {},
        'paint': {
            'fill-color': chex,
            'fill-opacity': 1.0
        }
    }


def make_response():
    spots = json.load(open('parking_spots.json'))
    coords = get_coords(spots)
    return [layer_for_spot(name, coord) for name, coord in coords]


all_data = load_data()


my_response = make_response()

import json

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        parsed_path = urlparse(self.path)
        print(parsed_path)
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes(json.dumps(my_response), "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

# run()

from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return (json.dumps(my_response), {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=True)
