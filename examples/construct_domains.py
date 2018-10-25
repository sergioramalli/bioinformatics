import os, sys, time, json
from pprint import pprint

#Imports configurations and add these modules to python enviroment 
from config import config
#imports custom build blast module 
from ebi.ebi import pfam

try:

	with open(config['pfam_domains'], 'r') as myfile:
		sequences = myfile.read()

	pfam = pfam()
	matched = pfam.construct(json.loads(sequences), config['query_sequences'])

	print();

except Exception as e:

	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, '\n', exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)
