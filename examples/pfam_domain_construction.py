import os, sys, time, json
from pprint import pprint

#Imports configurations and add these modules to python enviroment 
from config import config
#imports custom build blast module 
import blast.blast as blast
from ebi.ebi import pfam


# Sets whether to create a completely new blast database, set to True if you have an existing subject database
from_existing_db = True

try:

	blast = blast.local()
	blast.threads = config['threads']
	blast.iterations : config['iterations']
	
	# runs psiblast operation, and returns name of fasta file with Hits plus query 
	fasta = blast.set_db(config['subject_db'], config['subject_sequences']).run(config['query_sequences'], config['psi_results'], 20)

	print('Blast Finished')

	with open(config['psi_results_fasta'], 'r') as myfile:
		sequences = myfile.read()

	pfam = pfam()
	result = pfam.setEvalue('0.1').setSequence(sequences).submitSequence('iuriramalli@hotmail.com', 'api test')
	result = pfam.retrieve()['out']

	with open(config['pfam_domains'], "w") as text_file:

		text_file.write(result)

	print('Pfam Finished');

	with open(config['pfam_domains'], 'r') as myfile:
		sequences = myfile.read()

	matched = pfam.construct(json.loads(sequences), config['query_sequences'])

	with open(config['pfam_processed_domains'], "w") as text_file:

		json.dump(matched, text_file)

	print('Domain matching finished')

except Exception as e:

	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)

print('job successful')