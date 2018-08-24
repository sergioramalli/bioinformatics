#!/usr/bin/env python3
import csv
import os
import shutil
from Bio import SeqIO

class local(object):

	directory = '';
	query = '';
	db = '';
	psi_result = 'result.tab';
	threads = 4;
	iterations = 1;
	subject_db_label = 'subject_db_label'

	def __str__(self):

		return self.query

	def __getitem__(self, key):
		
		return getattr(self,key)

	def _run_psi(self):
		
		try:

			os.system("psiblast -query " + self.query + " -db " + self.subject_db_label + " -show_gis -outfmt 10 -num_iterations "+ str(self.iterations) +" -num_threads "+ str(self.threads) +" -num_alignments 1000 -dbsize 100000000 -comp_based_stats F -seg no -out " + self.psi_result );
			
		except Exception as e:

			raise(e)

		return self

	def _set_query(self, query):

		self.query = query
		return self

	def _matches(self, total = 29):

		try:

			f = open(self.psi_result, 'r')
			reader = csv.reader(f)

			x = 0
			subjects = []
			for row in reader:

				try:
					subjects.append( row[1] )
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

			for record in SeqIO.parse(self.subject_sequences, "fasta"):

				if record.id in subjects:

					if record.id not in ids:
						subjects_full.append(record)
						ids.append(record.id)
						x += 1
						if x > total:
							break

		except Exception as e:

			raise(e)

		try:

			SeqIO.write(subjects_full, self.psi_fasta, "fasta")

		except Exception as e:

			raise(e)

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

			os.makedirs(os.path.dirname(output), exist_ok=True)
			self.psi_result = output
			self.psi_fasta  = output + ".fasta"

			self._set_query(query)._run_psi()

		except Exception as e:

			print('Running blast error: ', str(e))
			os._exit(0)

		try:

			self._matches()
			return self.psi_fasta
			pass

		except Exception as e:

			print('Filtering blast results error: ', str(e))
			os._exit(0)

		return self




