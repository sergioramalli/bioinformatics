import json, os, csv
from config import config, system_config, output_files
from auth import process

file = open(output_files['analysis'], "r")
data = json.load(file)

process = process();
maxDomains = process.getMaxDomain(data);

ob = {}
x = 0
for query, domains1 in data.items():

	for hit, domains2 in data.items():

		sc = process.domain_similarity(domains1['pfam'], domains2['pfam'], maxDomains);
		js = process.js_score(domains1['pfam'], domains2['pfam'], maxDomains);
		x += 1
		ob[x] = {'query' : domains1['key'], 'hit' : domains2['key'], 'score' : sc, 'js' : js}

with open(output_files['distant_score_csv'], 'w') as csvfile:

	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['Query ID', 'Hit ID', 'Distance'])
	
	for key, value in ob.items() :

		distance = process.highest_score - value['score']
		if value['query'] == value['hit']:

			distance = 0

		filewriter.writerow([value['query'], value['hit'], distance])

with open(output_files['distant_full_csv'], 'w') as csvfile:

	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['Query ID', 'Hit ID', 'JS', 'Score',  'Distance'])
	
	for key, value in ob.items() :

		distance = process.highest_score - value['score']
		js = value['js']
		score = value['score'];
		if value['query'] == value['hit']:

			distance = 0 
			score = 0
			js = 0

		filewriter.writerow([value['query'], value['hit'], js, score, distance])

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from knee import KneeLocator
import pickle

csv = pd.read_csv(output_files['distant_score_csv'])
X = np.array(csv)

ssd = []
K = range(1,15)
for k in K:

    km = KMeans(n_clusters=k)
    km = km.fit(X)
    ssd.append(km.inertia_)

x = range(1, len(ssd)+1)
kn = KneeLocator(x, ssd, curve='convex', direction='decreasing',  S=1.0)
clusters = kn.knee

kmeans = KMeans(n_clusters=clusters)
kmeans.fit(X)

# It is important to use binary access
with open(output_files['kmeans_model'], 'wb') as f:
    pickle.dump(kmeans, f)



