#!/usr/bin/env python3
import os, shutil, re, csv, sys
from Bio import SeqIO

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]) + '/modules/')


class cogs(object):

	directory = '';
	query = {};
	cogs = {};
	threads = 4;
	output = "result.COG.csv"
	software_path = str(Path(__file__).parents[0]) + '/'

	"""docstring for cogs"""
	def __init__(self, directory, output = 'result.GOG.csv', reset = 'reset'):

		super(cogs, self).__init__()
		self.output = output
		self.directory = directory
		self._createDirectory(reset);

	def _createDirectory(self, reset = 'reset'):
		
		if reset == 'reset' :

			try:

				if os.path.exists(self.directory):
					shutil.rmtree(self.directory)

				pass

			except Exception as e:

				pass

		try:

			if not os.path.exists(self.directory):
			    os.makedirs(self.directory)
			    os.makedirs(self.directory + "BLASTss")
			    os.makedirs(self.directory + "BLASTno")
			    os.makedirs(self.directory + "BLASTff")
			    os.makedirs(self.directory + "BLASTcogn")
			    os.makedirs(self.directory + "BLASTconv")

			pass

		except Exception as e:

			print(str(e))
			os._exit(1)

	def _fixFiles(self):

		if os.path.exists(self.query['csv']):
			os.remove(self.query['csv'])
		## Python will convert \n to os.linesep

		if not os.path.exists(self.query['csv']):
		    with open(self.query['csv'], 'w'): pass

		f = open(self.query['csv'],'w')

		x = 0;
		for record in SeqIO.parse(self.query['sequences'], "fasta"):

			desc = record.description
			if "[" not in record.description:
				continue;

			genome = desc[desc.find('[')+1: desc.find(']') ]
			genome = genome.replace(' ', '_');
			line = record.id + ',' + genome.split(".")[0];

			f.write(line + '\n') #Give your csv text here.


	def _cogsDb(self):

		os.system("makeblastdb -in " + self.cogs['sequences'] + " -dbtype prot -out " + self.cogs['db'] );
		

	def _queryDb(self):
		
		os.system("makeblastdb -in " + self.query['sequences'] + " -dbtype prot -logfile " + self.directory + "queryBlastLog.log -out " + self.query['db'] );


	def _cogsBlast(self):
	
		os.system("psiblast -query " + self.query['sequences'] + " -db " + self.query['db'] + " -show_gis -outfmt 7 -num_threads "+ str(self.threads) +" -num_alignments 10 -dbsize 100000000 -comp_based_stats F -seg no -out " + self.directory + "BLASTss/QuerySelf.tab" );
		os.system("psiblast -query " + self.query['sequences'] + " -db " + self.cogs['db'] + " -show_gis -outfmt 7 -num_threads "+ str(self.threads) +" -num_alignments 1000 -dbsize 100000000 -comp_based_stats F -seg no -out " + self.directory + "BLASTno/QueryCOGs.tab" );
		os.system("psiblast -query " + self.query['sequences'] + " -db " + self.cogs['db'] + " -show_gis -outfmt 7 -num_threads "+ str(self.threads) +" -num_alignments 1000 -dbsize 100000000 -comp_based_stats T -seg yes -out " + self.directory + "BLASTff/QueryCOGs.tab" );

	def _runCognitor(self):

		os.system("cat " + self.query['csv'] + " " + self.cogs['csv'] + " > " + self.directory + "tmp.p2o.csv");

		os.system(self.software_path + "COG_software/COGmakehash/COGmakehash -i=" + self.directory + "tmp.p2o.csv -o=" + self.directory + "BLASTcogn -s=',' -n=1" );
		os.system(self.software_path + "COG_software/COGreadblast/COGreadblast -d=" + self.directory + "BLASTcogn -u=" + self.directory + "BLASTno -f=" + self.directory + "BLASTff -s=" + self.directory + "BLASTss -e=0.1 -q=2 -t=2" );
		os.system(self.software_path + "COG_software/COGcognitor/COGcognitor -i=" + self.directory + "BLASTcogn -t=" + self.cogs['csv'] + " -q=" + self.query['csv'] + " -o=" + self.output  );

	def setQuery(self, sequences):

		self.query = {'db' : self.directory + os.path.splitext(sequences)[0], 'sequences' : sequences, 'csv' :  self.directory + os.path.splitext(sequences)[0] + ".csv"}
		self._queryDb();

	def setCogs(self, sequences, csv, db = '', createDb = True ):

		# ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/prot2003-2014.fa.gz
		#ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/cog2003-2014.csv
		if db == '':

			self.cogs = {'sequences' : sequences, 'csv' : csv, 'db' : self.directory + 'COGs'}

		else:
			self.cogs = {'sequences' : sequences, 'csv' : csv, 'db' : db}

		if createDb == True:
			self._cogsDb();


	def setDirectory(self, directory):

		self.directory = directory;

	def cognitor(self):

		try:

			self._fixFiles();
			self._cogsBlast();
			self._runCognitor();
			pass

		except Exception as e:

			print(e);
			exit();

		finally:

			try:

				shutil.move("conflict.txt", self.directory + "conflict.txt")
				shutil.move("cognitor.log", self.directory + "cognitor.log")
				pass

			except Exception as e:

				pass;

