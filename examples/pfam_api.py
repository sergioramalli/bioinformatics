import os, sys, time
from pprint import pprint

#Imports configurations and add these modules to python enviroment 
from config import config
#imports custom build blast module 
from ebi.ebi import pfam

retrieve_existing_job = False
# 85 sequences limit 

try:

	with open(config['psi_results_fasta'], 'r') as myfile:
		sequences = myfile.read()

	try:

		pfam = pfam()
		if retrieve_existing_job == False:


			result = pfam.setEvalue('0.1').setSequence(sequences).submitSequence('iuriramalli@hotmail.com', 'api test')

		else: 

			pfam.job_id = config['pfam_job_id']
			pass

	except Exception as e:

		print('pfam error: ', e)
		os._exit(0) 

	finally:

		try:

			result = pfam.retrieve()['out']
			pass

		except Exception as e:

			print('retrieving pfam domains error: ', str(e))
			os._exit(0) 

except Exception as e:

	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)

try:

	with open(config['pfam_domains'], "w") as text_file:

		text_file.write(result)

except Exception as e:

	print('writing pfam domains error: , ', str(e))
	os._exit(0)

print('Pfam job finished - ', pfam.job_id);
