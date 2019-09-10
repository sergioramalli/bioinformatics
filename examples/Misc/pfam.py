import os, sys, time, json, shutil
from pprint import pprint

#Imports configurations and add these modules to python enviroment 
from config import config, system_config, output_files
import hashlib

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
