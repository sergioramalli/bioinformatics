import json, os, csv
from config import config, system_config, output_files
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from auth import process
from collections import Counter


process = process();

with open(output_files['kmeans_model_2'], 'rb') as f:
	km = pickle.load(f)

file = open(output_files['analysis'], "r")
data = json.load(file)

clusters = km.labels_

maxDomains = process.getMaxDomain(data);
minDomains = process.getMinDomain(data);

cl = {1 : {}, 0: {}, 2 : {}}
for key, value in data.items():

	cl[value['cluster']][value['key']] = value
	pass


total = 0
for query, domains1 in cl[0].items():

	for hit, domains2 in cl[0].items():

		total += process.js_score(domains1['pfam'], domains2['pfam'], maxDomains);

	break;

print('cluster-0', round(total / len(cl[0]), 7));

l_domains = []
l_cogs = []
for query, domains in cl[0].items():

	l_cogs.append(domains['cogs']['cog_id']);
	for key, value in domains['pfam']['info'].items():
		l_domains.append(key)

	pass

print(Counter(l_domains));
print(Counter(l_cogs));

print()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


total = 0
for query, domains1 in cl[1].items():

	for hit, domains2 in cl[1].items():

		total += process.js_score(domains1['pfam'], domains2['pfam'], maxDomains);

	break;

print('cluster-1', round(total / len(cl[1]), 7));

l_domains = []
l_cogs = []
for query, domains in cl[1].items():

	if 'cogs' in domains:
		l_cogs.append(domains['cogs']['cog_id']);

	for key, value in domains['pfam']['info'].items():
		l_domains.append(key)

	pass

print(Counter(l_domains));
print(Counter(l_cogs));
print()

total = 0
for query, domains1 in data.items():

	for hit, domains2 in data.items():

		total += process.js_score(domains1['pfam'], domains2['pfam'], maxDomains);

	break;
print(round(total / len(data), 7) );


l_domains = []
l_cogs = []
for query, domains in data.items():

	if 'cogs' in domains:
		l_cogs.append(domains['cogs']['cog_id']);

	for key, value in domains['pfam']['info'].items():
		l_domains.append(key)

	pass

print(Counter(l_domains));
print(Counter(l_cogs));

print()
print('MAX Domains', maxDomains);
print('Min Domains', minDomains);