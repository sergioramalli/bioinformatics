import os, sys, time
from pprint import pprint

#Imports configurations and adds important custom modules to python enviroment 
from config import config
#imports custom build blast module 
import blast.blast as blast

# Sets whether to create a completely new blast database, set to True if you have an existing subject database
from_existing_db = True

try:

	blast = blast.local()
	blast.threads = config['threads']
	blast.iterations : config['iterations']

	if from_existing_db != True:

		# runs psiblast operation, spins out new subject database and returns name of fasta file with hits plus query
		fasta = blast.make_db(config['subject_db'], config['subject_sequences']).run(config['query_sequences'], config['psi_results'], 30)

	else:

		# runs psiblast operation, and returns name of fasta file with Hits plus query 
		fasta = blast.set_db(config['subject_db'], config['subject_sequences']).run(config['query_sequences'], config['psi_results'], 50)


except Exception as e:

	print('blast fail')
	os._exit(0);
