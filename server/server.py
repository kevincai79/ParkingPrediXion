#!/usr/bin/env python

from collections import namedtuple
from datetime import datetime, timedelta
from flask import Flask, request
import calendar
import json
import numpy as np
import os
import pickle


def get_timestamps(evts):
	return [c['timestamp'] for c in evts['content']]


def get_bucket(dt):
	return dt.weekday() * 24 + dt.hour


AllData = namedtuple('AllData', ['spots', 'trends', 'total'])


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
    return '#%02x%02x%02x' % tuple(color_tuple)


def layer_for_spot(name, coords, dt):
    try:
        idx = all_data.spots.index(name)
    except:
        idx = None

    bucket = get_bucket(dt)

    errc = (200, 200, 200)
    full = (255, 0, 0)
    free = (0, 255, 0)
    unavail = errc

    if idx is not None:
        act = all_data.trends[bucket][idx]
        tot = all_data.total[idx]
        pct = act / float(tot)

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


all_data = load_data()
spots = json.load(open('parking_spots.json'))
coords = get_coords(spots)


def make_response(target_coord, dt):
    return [layer_for_spot(name, coord, dt) for name, coord in coords]


def norm(a, b):
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) 


def get_center(coords):
    return np.mean(np.array(coords), axis=0)


LocalStat = namedtuple('LocalStat', ['loc_idx', 'dist', 'center', 'freeness'])


def compute_local_stats(target, dt, hours_ahead=2):
    stats = []
    buckets = [get_bucket(dt + timedelta(hours=i)) for i in range(hours_ahead + 1)]
    for name, coord in coords:
        try:
            idx = all_data.spots.index(name)
        except:
            continue
        center = get_center(coord)
        dist = norm(target, center)
        freeness = [all_data.trends[bucket][idx] for bucket in buckets]
        freeness = [x if not np.isnan(x) else 0 for x in freeness]
        stats.append(
	    LocalStat(loc_idx=idx, dist=dist, center=tuple(center), freeness=freeness))
    stats.sort(key=lambda x: x.dist)
    return stats


def find_closest(local_stats):
    import numpy as np
    min_d = np.inf
    min_idx = None
    for idx, dist, freeness in local_stats:
       if dist < min_d:
           min_d = dist
           min_idx = idx
    return min_idx


def compute_suggestions(coord, ts):
    hours_ahead = 2
    dt = datetime.utcfromtimestamp(ts)
    stats = compute_local_stats(coord, dt, hours_ahead=hours_ahead)
    closest_coord = stats[0].center
    zones = make_response(coord, dt)
    # closest
    closest = stats[0]
    # freest nearby by hour
    nearby = stats[1:5]
    freests = [
        sorted(nearby, key=lambda x: -x.freeness[i])[0]
	for i in range(hours_ahead + 1)
    ]
    # find freest in a few hours
    best_freeness = 0
    best_hour = 0
    for hour in range(hours_ahead + 1):
        freeness = freests[hour].freeness[hour]
        if freeness > best_freeness:
            best_freeness = freeness
            best_hour = hour

    suggestions = [
	    {
		'long': closest.center[0],
		'lat': closest.center[1],
		'ts': ts,
		'msg': 'Closest parking zone, %.1f spots available.' % float(closest.freeness[0])
	    },
    ]
    if freests[0].freeness[0] > closest.freeness[0]:
        suggestions.append(
	    {
		'long': freests[0].center[0],
		'lat': freests[0].center[1],
		'ts': ts,
		'msg': 'Best nearby parking lot, %.1f spots available now.' % float(freests[0].freeness[0])
	    }
	)
        if best_hour > 0:
            suggestions.append({
                'long': freests[best_hour].center[0],
	        'lat': freests[best_hour].center[1],
	        'ts': ts + best_hour * 3600,
	        'msg': 'If you leave in %d hour%s, this zone will have %.1f spots.' % (
	            best_hour,
	            's' if best_hour > 1 else '',
	            float(freests[best_hour].freeness[best_hour]))
            })

    return {
	'suggestions': suggestions,
        'zones': zones,
    }


app = Flask(__name__)


@app.route('/')
def index():
    coord = (float(request.args['long']), float(request.args['lat']))
    ts = int(request.args['ts'])
    full_response = compute_suggestions(coord, ts)
    return (json.dumps(full_response), {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=True)
