import os, sys, time, json
from pprint import pprint
import csv

#Imports configurations and add these modules to python enviroment 
from config import config
#imports custom build blast module 
from cogs.cognitor import cogs

output = '../results/actinobacteria/results.COG.csv';

print('cogs started')
# example usage 
cogs = cogs('../results/actinobacteria/cogs/', output);
cogs.threads = 12;

cogs.setQuery("../results/actinobacteria/psi_example.fasta");
cogs.setCogs("../genomes/cogs.fa", "../genomes/cogs.p2o.csv", "../genomes/COGs", False);
cogs.cognitor();


with open(config['psi_results'] + "_blast.json", 'r') as myfile:

	sequences = json.load(myfile)
	sequences['cog'] = {'query' : './results/actinobacteria/psi_example.fasta', 'cogs' : "../genomes/cogs.fa", 'results' : output};

f = open(output, 'r')
reader = csv.reader(f)

for row in reader:
	
	key = row[0]
	sequences['sequences'][key]['cogs'] = {'score' : row[4], 'cog_id' : row[5]};

print(sequences)
with open(config['psi_results'] + "_blast.json", 'w') as outfile:
	json.dump(sequences, outfile, indent=4)

f.close()
print('results outputted into', output);
