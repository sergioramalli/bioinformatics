import os, sys, time
from pprint import pprint

#Imports configurations and add these modules to python enviroment 
from config import config
#imports custom build blast module 
from cogs.cognitor import cogs


# example usage 
cogs = cogs();
cogs.threads = 12;
cogs.results = '../results/NP_414543_1/result.COG.csv';

cogs.setDirectory('../results/actinobacteria/cogs/');
cogs._createDirectory();
cogs.setQuery("../results/actinobacteria/psi_example.fasta");
cogs.setCogs("../genomes/cogs.fa", "../genomes/cogs.p2o.csv", "../genomes/COGs", False);
cogs.cognitor();
