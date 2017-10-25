import json
import numpy as np


def get_coords(data):
	coords = []
	for l in data["content"]:
	    coord = [list(reversed([float(c) for c in pt.split(':')])) for pt in l["coordinates"].split(',')]

	    #if coord[0][0] > -100:
	    if l['locationUid'] == 'LOCATION-324':
	    	coords.append(coord)
	return np.array(coords)


def get_size(coord):
	return (coord[1][0] - coord[0][0], coord[1][1] - coord[0][1])


def get_edges(all_coords):
	x  = np.concatenate([coords.reshape((-1, 2)) for coords in all_coords])
	return np.array((np.min(x, axis=0), np.max(x, axis=0)))


def normalize(coords, edges):
	size = max(get_size(edges))
	return (coords - edges[(0, ) * coords.shape[1], :]) / size


locations = json.load(open('locations.json'))
spots = json.load(open('parking_spots.json'))

coords = get_coords(locations)
park_coords = get_coords(spots)

edges = get_edges((coords, park_coords))

norm_coords = coords  # normalize(coords, edges)
norm_park_coords = park_coords  # normalize(park_coords, edges)


import mplleaflet
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()

fig1, ax1 = plt.subplots()
if True:
	for coord in norm_coords:
		ax1.add_patch(
			patches.Rectangle(
				(coord[0][0], coord[0][1]),
				coord[1][0] - coord[0][0],
				coord[1][1] - coord[0][1], color='r'))

r = 20
lon = 2.363561
lat = 48.951918
#regpol1 = mpl.patches.RegularPolygon((lon, lat), 16, radius=r, color = 'r')
#ax1.add_patch(regpol1)

for coord in norm_park_coords:
	ax1.add_patch(patches.Polygon(coord, color='b'))

mplleaflet.show(fig = ax1.figure)

import sys
sys.exit(0)
