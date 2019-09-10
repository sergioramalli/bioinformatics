import os, sys, time, json, shutil, csv, hashlib
from pprint import pprint

#Imports configurations and adds important custom modules to python enviroment 
from config import config, system_config, output_files

from auth import process

import blast.blast as blast
from cogs.cognitor import cogs

try:

	# ensure folder is deleted first as it affects results

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

try:

	os.makedirs(output_files['interscan'], exist_ok=True)
	os.system("../modules/interproscan/interproscan.sh -appl Pfam-32.0 -i " + output_files['blast_fasta'] + " -f json -f tsv -b " + output_files['interscan_pfam'] + " -iprlookup false -dra false");

	with open(output_files['interscan_pfam_json'], 'r') as myfile:

		domains = {};
		reader = json.load(myfile)
		for x in reader['results']:

			sID = hashlib.md5(x['xref'][0]['id'].encode('utf-8')).hexdigest()
			domains[sID] = {'start' : 0, 'end' : 0, 'info' : {}, 'sequence' : x['sequence'], 'domains' : [ ]}
			pass

		for x in reader['results']:

			sID = hashlib.md5(x['xref'][0]['id'].encode('utf-8')).hexdigest()

			for xx in x['matches']:

				if domains[sID]['end'] >  xx['locations'][0]['start']:

					pass;

				else:	

					domains[sID]['domains'].append(xx['signature']['accession']) 
					domains[sID]['info'][xx['signature']['accession']] = {'evalue' : xx['locations'][0]['evalue'], 'score' : xx['locations'][0]['score'], 'start' : xx['locations'][0]['start'], 'end' : xx['locations'][0]['end']}

				domains[sID]['start'] = xx['locations'][0]['start']
				domains[sID]['end'] = xx['locations'][0]['end']

			pass


		query = domains[list(domains.keys())[0]]

	for key, value in domains.items():

		domains[key].pop('end', None)
		domains[key].pop('start', None)  

	with open(output_files['blast_json'], 'r') as the_file:

		reader = json.load(the_file)
		for key, value in domains.items():

			if key in reader:
				reader[key]['pfam'] = value;
			else:
				print(key);


	with open(output_files['interscan_pfam_json'], 'w') as the_file:
	    the_file.write(json.dumps(reader, indent=4))

except Exception as e:

	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)


# Sets-up the class and creates a directory for all the temp files. 
cogs = cogs(output_files['cogs'], output_files['cogs_csv']);
cogs.threads = config['threads'];

 # query sequence you want to check against  
cogs.setQuery(output_files['blast_fasta']);

# sets and/or creates the database of sequences to run your analysis against. 
cogs.setCogs(system_config['cogs_fasta'], system_config['cogs_p2o'], system_config['cogs_genomes_cogs'], config['create_cogs_db']);

# starts analysis 
cogs.cognitor();

with open(output_files['interscan_pfam_json'], 'r') as myfile:

	sequences = json.load(myfile)

f = open(output_files['cogs_csv'], 'r')
reader = csv.reader(f)

for row in reader:

	key = hashlib.md5(row[0].encode('utf-8')).hexdigest()
	sequences[key]['cogs'] = {'score' : row[4], 'cog_id' : row[5]};

process = process();
sequences = process.processData(sequences)

with open(output_files['final'], 'w') as outfile:
	json.dump(sequences, outfile, indent=4)

f.close()
print('results outputted into', output_files['final']);

domains = {}
l_domains = {}
for key, values in sequences.items():

	for dKey, dvalues in values['pfam']['info'].items():

		if dKey in domains:

			if dvalues['score'] > domains[dKey]:
				domains[dKey] = dvalues['score']

			if dvalues['score'] < l_domains[dKey]:
				l_domains[dKey] = dvalues['score']

		else:

			l_domains[dKey] = dvalues['score']
			domains[dKey] = dvalues['score'];

for key, values in sequences.items():

	total = 0;
	x = 1;
	for dKey, dvalues in values['pfam']['info'].items():

		xx = dvalues['score'] - l_domains[dKey];
		yy = dvalues['score'] - l_domains[dKey];

		if yy == 0:

			sequences[key]['pfam']['info'][dKey]['n_norm_score'] = 0

		else:

			sequences[key]['pfam']['info'][dKey]['n_norm_score'] = (xx) / (yy)

		sequences[key]['pfam']['info'][dKey]['o_norm_score'] = (dvalues['score']) /  (domains[dKey])


with open(output_files['analysis'], 'w') as outfile:
	json.dump(sequences, outfile, indent=4)
