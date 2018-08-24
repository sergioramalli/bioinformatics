#!/usr/bin/env python3
import csv
import os
import shutil
from Bio import SeqIO

class localBlast(object):

	directory = '';
	query = '';
	db = '';
	psi_result = 'result.tab';
	threads = 4;
	iterations = 1;
	subject_db = 'subject_db'

	def __str__(self):

		return self.query

	def __getitem__(self, key):
		
		return getattr(self,key)


	def _runBlast(self):
		
		os.system("psiblast -query " + self.query + " -db " + self.subject_db + " -show_gis -outfmt 10 -num_iterations "+ str(self.iterations) +" -num_threads "+ str(self.threads) +" -num_alignments 1000 -dbsize 100000000 -comp_based_stats F -seg no -out " + self.psi_result );
		return self

	def _setQuery(self, sequences):

		self.query = sequences
		return self

	def _makeDb(self, db = '' ):

		try:

			if db == '':

				self.subject_db = self.directory + self.subject_db
				os.system("makeblastdb -in " + self.subject_sequences + " -dbtype prot -out "+ self.subject_db  );

			else:

				self.subject_db = db

			return self
			pass

		except Exception as e:
			
			print('Error', e)
			os._exit(0)

	def _setDirectory(self, directory):

		self.directory = directory;
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

		return self

	def run(self, directory, query, subject_sequences, subject_db = '', ):

		try:

			if subject_sequences != '':
				self.subject_sequences = subject_sequences

			self._setDirectory(directory)._setQuery(query)._makeDb(subject_db)._runBlast()

			pass

		except Exception as e:

			print('Error: ', e)
			os._exit(0)

		return self

	def matches(self, fasta, total = 29):

		self.fasta = fasta
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

		try:
			
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

			print(str(e))
			os._exit(0)

		try:

			SeqIO.write(subjects_full, self.fasta, "fasta")

		except Exception as e:

			print('Fasta writing error, ', str(e))
			os._exit(0)


		return self


