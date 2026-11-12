import json
import math
import time
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
import matplotlib.pyplot as plt
import requests                         
from matplotlib.colors import to_hex
import re

BASE_DIR = Path('C:/_saki/work/_misc/orbit_workshop')  
IN_DIR = BASE_DIR / 'IN'
OUT_DIR = BASE_DIR / 'OUT'
IN_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

MU_EARTH_KM3_S2 = 398600.4418 #earth gravity (km^3/s^2)
EARTH_RADIUS_KM = 6378.137 #earth equatorial radius (km), used as a sphere

STEP_SECONDS = 5 #propagation time step (s)
DURATION_HOURS = 24 #prop. window (h)
LIVE_GROUP = None #

#print(f"Window: {DURATION_HOURS} h at {STEP_SECONDS} s steps | live data: {LIVE_GROUP or 'off (workshop snapshot)'}")
#print(f"IN_DIR:  {IN_DIR}\nOUT_DIR: {OUT_DIR}")


#orb_elem = open("orbital_elements.json") 
#data_mani = open("data_manifest.json")

def read_gp_json(f): #peram is filename string  
	words = ["OBJECT_NAME", "NORAD_CAT_ID", "EPOCH", "MEAN_MOTION", "ECCENTRICITY", "INCLINATION", "RA_OF_ASC_NODE", "ARG_OF_PERICENTER", "MEAN_ANOMALY"]

	#opens as dict
	with open(f) as json_file:
		sats = json.load(json_file)

	#print(sats[0])

	for i in sats: 
		for w in words:
			if w not in i:
				print("false")
				raise ValueError("record missing required key")
			#else: 
				#print("true", w)
	return sats

	
def parse_gp_epoch(utc): 
	return datetime.fromisoformat(utc.rstrip('Z')).replace(tzinfo=timezone.utc)

def parse_gp_elements(rec): 
	#print(type(rec))

	n = 2 * math.pi * rec['MEAN_MOTION'] / 86400              #mean motion: rev/day -> rad/s
	name, norad_id = rec['OBJECT_NAME'], int(rec['NORAD_CAT_ID'])
	
	return{
		'name': name,
        'norad_id': norad_id,
        'label': f"{name} [{norad_id}]",
        'epoch': parse_gp_epoch(rec['EPOCH']),
        'n_rad_s': n,
        'a_km': (MU_EARTH_KM3_S2 / n ** 2) ** (1 / 3), #kepler's third law
        'e': rec['ECCENTRICITY'], 
        'i_rad': math.radians(rec['INCLINATION']),
        'raan_rad': math.radians(rec['RA_OF_ASC_NODE']),
        'argp_rad': math.radians(rec['ARG_OF_PERICENTER']),
        'M0_rad': math.radians(rec['MEAN_ANOMALY']),
	}


	def elems_table(elems): 

		

sats = read_gp_json("orbital_elements.json")
elems = [parse_gp_elements(i) for i in sats]

#elems.append()
#print(elems)
