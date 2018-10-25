import os, sys, time, json
from pprint import pprint

#Imports configurations and adds important custom modules to python enviroment 
from config import config
#imports custom build blast module 
import blast.blast as blast
from ebi.ebi import pfam

try:

	def jaccard_similarity(list1, list2):
		intersection = len(list(set(list1).intersection(list2)))
		union = (len(list1) + len(list2)) - intersection
		return float(intersection / union)

	blast = blast.local()
	blast.threads = config['threads']
	blast.iterations : config['iterations']

	# runs psiblast operation, and returns name of fasta file with Hits plus query 
	fasta = blast.set_db(config['subject_db'], config['subject_sequences']).run(config['query_sequences'], config['psi_results'], 1000)

	with open(fasta, 'r') as myfile:
		sequences = myfile.read()

	pfam = pfam()
	result = pfam.setEvalue('0.1').setSequence(sequences).submitSequence('iuriramalli@hotmail.com', 'api test')
	result = pfam.retrieve()['out']

	with open(config['pfam_domains'], "w") as text_file:

		text_file.write(result)

	print('Pfam Finished');

	with open(config['pfam_domains'], 'r') as myfile:
		sequences = myfile.read()

	print(config['query_sequences'])

	matched = pfam.construct(json.loads(sequences), config['query_sequences'])

	with open(config['pfam_processed_domains'], "w") as text_file:

		json.dump(matched, text_file)

	print('Domain matching finished')

	x = 0
	for key, value in matched.items():

		if x == 0:

			query_sequence = set(value['domains'].split(','));

		else : 

			subject_sequence = set(value['domains'].split(','));
			print(jaccard_similarity(query_sequence, subject_sequence))

		x += 1;
		pass


except Exception as e:

	print(e)
	print('blast fail')
	os._exit(0);

