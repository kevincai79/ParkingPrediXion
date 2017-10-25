import json
import numpy as np

def get_timestamps(evts):
	return [c['timestamp'] for c in evts['content']]


def get_bucket(dt):
	return dt.weekday() * 24 + dt.hour


from collections import namedtuple
AllData = namedtuple('AllData', ['spots', 'trends', 'total'])

def load_data():
	pass
