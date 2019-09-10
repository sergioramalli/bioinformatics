#!/usr/bin/env python3
import csv
import os
import shutil
import json
import sys

from Bio import SeqIO

def exp(e):
	
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(e, exc_type, fname, exc_tb.tb_lineno)
	os._exit(0)


class local(object):

	directory = '';
	query = '';
	db = '';
	psi_result = 'result.tab';
	threads = 4;
	iterations = 1;
	subject_db_label = 'subject_db_label'
	outfmt = 10
	num_alignments = 1000
	dbsize = 100000000

	def __str__(self):

		return self.query

	def __getitem__(self, key):
		
		return getattr(self,key)

	def _run_psi(self):
		
		try:

			os.system("psiblast -query " + self.query + " -db " + self.subject_db_label + " -show_gis -outfmt " + str(self.outfmt) + " -num_iterations "+ str(self.iterations) +" -num_threads "+ str(self.threads) +" -num_alignments " + str(self.num_alignments) + " -dbsize " + str(self.dbsize) + " -comp_based_stats F -seg no -out " + self.psi_result );
			
		except Exception as e:

			raise(e)

		return self

	def _set_query(self, query):

		self.query = query
		return self

	def _matches(self, total = 30):

		try:

			f = open(self.psi_result, 'r')
			reader = csv.reader(f)

			x = 0
			subjects = []
			jsonObject = {};
			jsonObject['blast'] = {'outfmt' : self.outfmt, 'engine' : 'psi-blast', 'query' : self.query, 'db' : self.subject_db_label, 'num_alignments' : self.num_alignments, 'dbsize' : self.dbsize, 'query' : self.query };
			jsonObject['sequences'] = {};

			for row in reader:

				try:

					# create json file here id = blast results 
					if x == 0:

						subjects.append( row[0] )
						jsonObject['sequences'][row[0]] = {}
						jsonObject['sequences'][row[0]]['blast'] = row
						jsonObject['sequences'][row[0]]['query'] = True

					else: 
					
						subjects.append( row[1] )
						jsonObject['sequences'][row[1]] = {}
						jsonObject['sequences'][row[1]]['blast'] = row
						jsonObject['sequences'][row[1]]['query'] = False

					if x >= total:
						break;

				except Exception as e:

					pass
				
				x += 1

			f.close()

			subjects_full = []
			ids = []
			x = 0
			for record in SeqIO.parse(self.query, "fasta"):

				ids.append(record.id)
				subjects_full.append(record)

				jsonObject['sequences'][record.id]['sequence'] = str(record.seq); 
				jsonObject['sequences'][record.id]['description'] = record.description; 
				jsonObject['sequences'][record.id]['name'] = record.name; 

			for record in SeqIO.parse(self.subject_sequences, "fasta"):

				if record.id in subjects:

					if record.id not in ids:

						# append the sequence, name, description and seq information here to the json object from above 
						jsonObject['sequences'][record.id]['sequence'] = str(record.seq); 
						jsonObject['sequences'][record.id]['description'] = record.description; 
						jsonObject['sequences'][record.id]['name'] = record.name; 
						subjects_full.append(record)
						ids.append(record.id)
						x += 1
						if x >= total:
							break


		except Exception as e:

			exp(e)

		try:

			with open(self.psi_json, 'w') as outfile:
				json.dump(jsonObject, outfile)

			SeqIO.write(subjects_full, self.psi_fasta, "fasta")

		except Exception as e:

			exp(e)

		return self

	def make_db(self, subject_db_label, subject_sequences):

		try:

			self.subject_db_label = subject_db_label
			self.subject_sequences = subject_sequences
			os.system( "makeblastdb -in " + self.subject_sequences + " -dbtype prot -out "+ self.subject_db_label );
			return self
			
		except Exception as e:
			
			print('Makeing Databse error: ', e)
			os._exit(0)

	def set_db(self, subject_db_label, subject_sequences):

		try:

			self.subject_db_label = subject_db_label
			self.subject_sequences = subject_sequences
			return self
			
		except Exception as e:
			
			print('setting database error: ', e)
			os._exit(0)

	def run(self, query, output, total = 29 ):

		try:

			os.makedirs(os.path.dirname(output['blast']), exist_ok=True)

			self.psi_result = output['blast_csv']
			self.psi_fasta  = output['blast_fasta']
			self.psi_json  = output['blast_json']

			self._set_query(query)._run_psi()

		except Exception as e:

			print('Running blast error: ', str(e))
			os._exit(0)

		try:

			self._matches(total)
			return self.psi_fasta
			pass

		except Exception as e:

			print('Filtering blast results error: ', str(e))
			os._exit(0)

		return self




