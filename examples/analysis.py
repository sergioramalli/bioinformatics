import json, os, csv
from config import config, system_config, output_files
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from auth import process

process = process();

with open(output_files['kmeans_model_2'], 'rb') as f:
	km = pickle.load(f)

file = open(output_files['analysis'], "r")
data = json.load(file)

clusters = km.labels_

x = 0; 
for key, value in data.items():

	data[key]['cluster'] = int(clusters[value['key']])
	x += 1

with open(output_files['analysis'], 'w') as outfile:
	json.dump(data, outfile, indent=4)

cl = {}
for key, value in data.items():

	if value['key'] == 0:
		cluster = value['cluster']
		cogs = value['cogs']['cog_id']

	if value['cluster'] == cluster:

		cl[key] = value

	pass

maxDomains = process.getMaxDomain(data);

total = 0
for query, domains1 in cl.items():

	for hit, domains2 in cl.items():

		total += process.js_score(domains1['pfam'], domains2['pfam'], maxDomains);

	break;

print(round(total / len(cl), 5));

total = 0
for query, domains1 in data.items():

	for hit, domains2 in data.items():

		total += process.js_score(domains1['pfam'], domains2['pfam'], maxDomains);

	break;

print(round(total / len(data), 5) );