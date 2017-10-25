import http.client
import json
import data

conn = http.client.HTTPSConnection("ic-event-service.run.aws-usw02-pr.ice.predix.io")

headers = {
    'authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIyOGQ2NmJmZGRlODM0OTlkYTJiNjhlNzE2ZTU5YjJlOSIsInN1YiI6ImhhY2thdGhvbiIsInNjb3BlIjpbInVhYS5yZXNvdXJjZSIsImllLWN1cnJlbnQuU0RTSU0tSUUtUFVCTElDLVNBRkVUWS5JRS1QVUJMSUMtU0FGRVRZLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEVERVNUUklBTi5JRS1QRURFU1RSSUFOLkxJTUlURUQuREVWRUxPUCJdLCJjbGllbnRfaWQiOiJoYWNrYXRob24iLCJjaWQiOiJoYWNrYXRob24iLCJhenAiOiJoYWNrYXRob24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjlmMWYyYzRkIiwiaWF0IjoxNTA4OTUxOTAxLCJleHAiOjE1MDk1NTY3MDEsImlzcyI6Imh0dHBzOi8vODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3LnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3IiwiYXVkIjpbImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBBUktJTkcuSUUtUEFSS0lORy5MSU1JVEVEIiwiaWUtY3VycmVudC5TRFNJTS1JRS1QVUJMSUMtU0FGRVRZLklFLVBVQkxJQy1TQUZFVFkuTElNSVRFRCIsInVhYSIsImhhY2thdGhvbiIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBFREVTVFJJQU4uSUUtUEVERVNUUklBTi5MSU1JVEVEIl19.l43KxrRA9HnxvU0w476VN3hfLeo8vRBdIngFd4QC0VG_ZLh_MrlKhS22403ICTb8Gnb5qC6C9ogKNeNFkejDiULZkeACo0nB6jJ0gcSjEKl4AOLNDyw--STSHTe8gNe9dS6hT46rRceNJaOqL9CLjDIUMYyGNFpUgGbhzq8E4Ja1FWwcngsM7Q8ztXiEdRQKaEh0hsAunqTLlFmzSCsyb4YtNjubn3FVrWifqLAdmR9yc0jSy4es1tP97j_n_3GjJRZQ8J-axXUvMA39ViaVdI8UlCY550674zCghqn82vZWlP1Lhy85FDtmvzuqe9j0a-JUSC7EETSg2TxcGoiPXQ",
        'predix-zone-id': "SDSIM-IE-PARKING",
	    'cache-control': "no-cache",
	        'postman-token': "50d529af-3dc4-c70f-118b-9c12da121d0d"
		    }


import os.path


from datetime import datetime
import calendar


def get_timestamp(d):
	return 1000 * calendar.timegm(d.timetuple())

# params = 'eventType=%s&startTime=1508456827000&endTime=1508975227000' % (evt_type, )


# PKIN, PKOUT
def get_evt(location, evt_type, start_ts, end_ts):
	params = 'eventType=%s&startTime=%d&endTime=%d&pageSize=1000000' % (evt_type, start_ts, end_ts)
	
	key = location + '&' + params
	parsed = None
	if True and os.path.isfile(key):
		print('Returning from cache: %s' % key)
		try:
			parsed = json.load(open(key, encoding='utf-8'))
			if 'error' in parsed or 'error-code' in parsed:
				print('Invalid cache.')
				parsed = None
		except:
			print('Invalid cache.')
			pass
	if not parsed:
		addr = "/v2/locations/%s/events?%s" % (location, params)
		print(addr)
		conn.request("GET", addr, headers=headers)
		# conn.request("GET", "/v2/locations/LOCATION-324/events?eventType=PKIN&startTime=1508456827000&endTime=1508975227000&pageSize=10000000", headers=headers)

		res = conn.getresponse()
		data = res.read()
		raw = data.decode("utf-8")
		with open(key, 'w') as f:
			f.write(raw)
			print('Wrote to cache: %s' % key)
		parsed = json.loads(raw)
	if 'error' in parsed or 'error-code' in parsed:
		raise Exception(parsed)
	return parsed

	return json.loads(raw)


def get_location_list(data):
	return [l['locationUid'] for l in data['content'] if 'ATL' not in l['locationUid']]


start_ts = get_timestamp(datetime(2017, 10, 17, 23, 47, 0))
end_ts = get_timestamp(datetime(2017, 10, 24, 23, 47, 0))

def get_dt(ts):
	return datetime.utcfromtimestamp(ts / 1000.)


park_data = json.load(open('parking_spots.json'))
park_spots = get_location_list(park_data)
print(park_spots)

import time

blacklisted = ['LOCATION-324', 'LOCATION-297', 'LOCATION-290', 'LOCATION-184', 'LOCATION-282', 'LOCATION-276', 'LOCATION-233', 'LOCATION-225']

park_spots = [spot for spot in park_spots if spot not in blacklisted]

if False:
	for spot in park_spots:
		try:
			get_evt(spot, 'PKIN', start_ts, end_ts)
			get_evt(spot, 'PKOUT', start_ts, end_ts)
		except:
			print('Blacklisting : %s' % spot)
			blacklisted.append(spot)

print(blacklisted)

tf_data = json.load(open('locations.json'))
lanes = get_location_list(tf_data)
print(lanes)

# for lane in lanes:
#	 get_evt(lane, 'TFEVT', start_ts, end_ts)


def get_timestamps(evts):
	return [c['timestamp'] for c in evts['content']]


def get_bucket(dt):
	return dt.weekday() * 24 + dt.hour


import numpy as np
l = []
for loc_idx, loc in enumerate(park_spots):
	l += [(ts, loc_idx, 1) for ts in get_timestamps(get_evt(loc, 'PKIN', start_ts, end_ts))]
	l += [(ts, loc_idx, -1) for ts in get_timestamps(get_evt(loc, 'PKOUT', start_ts, end_ts))]
l.sort()
arr_ts = np.array([t[0] for t in l])

status = np.zeros(len(park_spots))

num_buckets = 24 * 8

trends = np.zeros((num_buckets, len(park_spots)), dtype=float)
counts = np.zeros((num_buckets, len(park_spots)))

status_series = np.zeros((len(l), len(park_spots)))
for evt_idx, (ts, loc_idx, delta) in enumerate(l):
	# dt = get_dt(ts)
	# bucket = get_bucket(dt)
	# trends[bucket, loc_idx] += status[loc_idx]
	# counts[bucket, loc_idx] += 1
	status_series[evt_idx, :] = status
	status[loc_idx] += delta


status_series -= np.min(status_series, axis=0)
total_avail = np.max(status_series, axis=0)
status_series = total_avail - status_series

for evt_idx, ((ts, loc_idx, delta), status) in enumerate(zip(l, status_series)):
	# print(loc_idx, status)
	dt = get_dt(ts)
	bucket = get_bucket(dt)
	trends[bucket, loc_idx] += status[loc_idx]
	counts[bucket, loc_idx] += 1

loc_idx = park_spots.index('LOCATION-281')
for loc_idx in range(len(park_spots)):
	print(trends[:, loc_idx])
	print(counts[:, loc_idx])
#	import pdb
#	pdb.set_trace()


trends = trends / counts

from collections import namedtuple
AllData = namedtuple('AllData', ['spots', 'trends', 'total'])

all_data = AllData(spots=park_spots, trends=trends, total=total_avail)
import pickle
all_pickled = pickle.dumps(all_data)

with open('all_data.p', 'wb') as f:
	f.write(all_pickled)
import matplotlib.pyplot as plt
plt.hold(True)
for loc_idx in range(len(park_spots)):
	plt.plot(trends[:, loc_idx])
plt.show()
