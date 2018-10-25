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

	pfam = pfam()
	result = pfam.setEvalue('0.1').setSequence(config['psi_results_fasta']).submitSequence('iuriramalli@hotmail.com', 'api test')
	# pfam.job_id = "pfamscan-R20181025-110658-0662-22547843-p1m"

	result = pfam.retrieve("out")
	matched = pfam.construct(config['psi_results'] + "_blast.json")

	with open(config['psi_results'] + "_blast.json", 'w') as outfile:
		json.dump(matched, outfile)


except Exception as e:

	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)

print('job successful')