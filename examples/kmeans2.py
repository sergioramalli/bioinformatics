import json, os, csv
from config import config, system_config, output_files
from auth import process

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from knee import KneeLocator
import pickle

import matplotlib.pyplot as plt

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
		cog = process.cogs(domains1['cogs'], domains2['cogs']);

		if domains1['key'] ==  domains2['key']:

			continue;

		x += 1
		ob[x] = {'query' : domains1['key'], 'hit' : domains2['key'], 'score' : sc, 'js' : js, 'cog' : cog}

	break;

with open(output_files['distant_score_csv_2'], 'w') as csvfile:

	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow([ 'JS', 'Score',  'Distance', 'cog'])
	
	for key, value in ob.items():

		filewriter.writerow([ value['js'], value['score'], process.highest_score - value['score'], value['cog'] ])

csv = pd.read_csv(output_files['distant_score_csv_2'])
X = np.array(csv)

ssd = []
K = range(1,10)
for k in K:

    km = KMeans(n_clusters=k)
    km = km.fit(X)
    ssd.append(km.inertia_)

x = range(1, len(ssd)+1)
kn = KneeLocator(x, ssd, curve='convex', direction='decreasing',  S=1.0)
clusters = kn.knee

# plt.plot(K, ssd, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Sum_of_squared_distances')
# plt.title('Elbow Method For Optimal k')
# plt.show()

kmeans = KMeans(n_clusters=clusters)
kmeans.fit(X)

# It is important to use binary access
with open(output_files['kmeans_model_2'], 'wb') as f:
    pickle.dump(kmeans, f)



