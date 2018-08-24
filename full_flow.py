from blast.blast import localBlast
from ebi.ebi import pfam
# from cogs.cognitor import cogs

import json
import platform, os, sys, time
from pprint import pprint

from Bio import SeqIO

subject_sequences = "genomes/actinobacteria.faa"
subject_db = "results/subject_db"
# subject_db = ""

query_sequences = 'queries/NP_414543_1_longer_than_subjects.faa'
query_id = "NP_414543.1" 
var = "NP_414543_1"

job_id = 'pfamscan-R20180824-150502-0381-53429376-p2m'
# job_id = '';

threads = 12;
psi_iterations = 1

results_directory = 'results/'
if not os.path.exists("results/" + var + "/"):
	os.makedirs("results/" + var + "/")

blast_results = "results/" + var + "/psi_results.faa"
pfam_matched_fasta = "results/" + var + "/pfam_domain_matched.faa"
pfam_domains_fasta = "results/" + var + "/pfam_domains.faa"

# try:

# 	db = localBlast()
# 	db.threads = threads
# 	db.iterations = psi_iterations
# 	db.psi_results = results_directory + "psi";

# 	blast_results = db.run(results_directory, query_sequences, subject_sequences, subject_db).matches(blast_results, 30)['fasta']
# 	pass

# except Exception as e:

# 	print('blast fail')
# 	os._exit(0);

try:

	with open(blast_results, 'r') as myfile:
		sequences = myfile.read()

	try:

		pfam = pfam()
		if job_id == '':

			result = pfam.setEvalue('0.1').setSequence(sequences).submitSequence('iuriramalli@hotmail.com', 'api test')

		else: 

			pfam.job_id = job_id
			pass

	except Exception as e:

		print('pfam error: ', e)
		os._exit(0) 

	finally:

		try:

			job_id = pfam.job_id
			result = pfam.retrieve()['out']
			pass

		except Exception as e:

			print('retrieving pfam: ', e)
			os._exit(0) 

except Exception as e:


	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)

print(job_id)


try:

	with open(pfam_domains_fasta, "w") as text_file:

		text_file.write(result)

except Exception as e:

	print('writing pfam domains, ', str(e))
	os._exit(0)

matched = pfam.construct(json.loads(result), query_id)

try:
	
	subjects_full = []
	for record in SeqIO.parse(subject_sequences, "fasta"):

		if record.id in matched:

			subjects_full.append(record)

except Exception as e:

	print(str(e))
	os._exit(0)

try:

	SeqIO.write(subjects_full, pfam_matched_fasta, "fasta")

except Exception as e:

	print('Fasta writing error, ', str(e))
	os._exit(0)
