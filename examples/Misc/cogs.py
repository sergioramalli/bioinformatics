import os, sys, time, json, csv, hashlib
from pprint import pprint

#Imports configurations and add these modules to python enviroment 
from config import config, system_config, output_files

from cogs.cognitor import cogs

# Sets-up the class and creates a directory for all the temp files. 
cogs = cogs(output_files['cogs'], output_files['cogs_csv']);
cogs.threads = config['threads'];

 # query sequence you want to check against  
cogs.setQuery(output_files['blast_fasta']);

# sets and/or creates the database of sequences to run your analysis against. 
cogs.setCogs(system_config['cogs_fasta'], system_config['cogs_p2o'], system_config['cogs_genomes_cogs'], config['create_cogs_db']);

# starts analysis 
cogs.cognitor();