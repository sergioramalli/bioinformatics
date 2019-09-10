import os, sys, time, json, shutil, hashlib
from pprint import pprint

#Imports configurations and adds important custom modules to python enviroment 
from config import config, system_config, output_files

import blast.blast as blast

try:

	blast = blast.local()
	blast.threads = config['threads']
	blast.iterations : config['iterations']

	if config['from_existing_db'] != True:

		# runs psiblast operation, spins out new subject database and returns name of fasta file with hits plus query
		fasta = blast.make_db(system_config['subject_db'], system_config['subject_sequences']).run(config['query'], output_files, config['hits'])

	else:

		# runs psiblast operation, and returns name of fasta file with Hits plus query 
		fasta = blast.set_db(system_config['subject_db'], system_config['subject_sequences']).run(config['query'], output_files, config['hits'])

	results = {}
	with open(output_files['blast_json'], 'r') as myfile:

		for key, value in json.load(myfile)['sequences'].items():

			sID = hashlib.md5(key.encode('utf-8')).hexdigest()
			results[sID] = {'blast' : {'id' : key, 'e-value': value['blast'][10], 'score' : value['blast'][11], 'sequence' : value['sequence'] }}

			pass

		pass

	with open(output_files['blast_json'], 'w') as the_file:
	    the_file.write(json.dumps(results))

except Exception as e:

	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)
