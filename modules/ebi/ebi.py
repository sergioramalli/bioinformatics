#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Python Client Automatically generated with:
# https://github.com/ebi-wp/webservice-client-generator
#
# Copyright (C) 2006-2018 EMBL - European Bioinformatics Institute
# Under GNU GPL v3 License - See LICENSE for more details!
###############################################################################

from __future__ import print_function
from xmltramp2 import xmltramp
from optparse import OptionParser
import platform, os, sys, time
import json
from Bio import SeqIO

try:

	from urllib.parse import urlparse, urlencode
	from urllib.request import urlopen, Request
	from urllib.error import HTTPError
	from urllib.request import __version__ as urllib_version
	
except ImportError:

	from urlparse import urlparse
	from urllib import urlencode
	from urllib2 import urlopen, Request, HTTPError
	from urllib2 import __version__ as urllib_version

# allow unicode(str) to be used in python 3
try:

  unicode('')

except NameError:

  unicode = str

class ebi():

	"""docstring for ClassName"""
	def __init__(self):

		self.checkInterval = 5;

	# Debug print
	def printDebugMessage(self, functionName, message, level):

		if(level <= self.debugLevel):

			print(u'[' + functionName + u'] ' + message, file=sys.stderr)

	# User-agent for request (see RFC2616).
	def getUserAgent(self):

		self.printDebugMessage(u'getUserAgent', u'Begin', 11)

		# Agent string for urllib2 library.
		urllib_agent = u'Python-urllib/%s' % urllib_version
		clientRevision = u'$Revision: 2107 $'
		clientVersion = u'0'
		if len(clientRevision) > 11:

			clientVersion = clientRevision[11:-2]

		# Prepend client specific agent string.
		user_agent = u'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
			clientVersion, os.path.basename( __file__ ),
			platform.python_version(), platform.system(),
			urllib_agent
		)

		self.printDebugMessage(u'getUserAgent', u'user_agent: ' + user_agent, 12)
		self.printDebugMessage(u'getUserAgent', u'End', 11)
		return user_agent

	# Wrapper for a REST (HTTP GET) request
	def restRequest(self, url):

		self.printDebugMessage(u'restRequest', u'Begin', 11)
		self.printDebugMessage(u'restRequest', u'url: ' + url, 11)

		try:

			# Set the User-agent.
			user_agent = self.getUserAgent()
			http_headers = { u'User-Agent' : user_agent }
			req = Request(url, None, http_headers)
			# Make the request (HTTP GET).
			reqH = urlopen(req)
			resp = reqH.read()
			contenttype = reqH.info()

			if(len(resp)>0 and contenttype!=u"image/png;charset=UTF-8"

			   and contenttype!=u"image/jpeg;charset=UTF-8"
			   and contenttype!=u"application/gzip;charset=UTF-8"):

				result = unicode(resp, u'utf-8')
			else:

				result = resp

			reqH.close()

		# Errors are indicated by HTTP status codes.
		except HTTPError as ex:

			print(xmltramp.parse(ex.read())[0][0])
			quit()

		self.printDebugMessage(u'restRequest', u'End', 11)

		return result

	# Submit job
	def serviceRun(self, email, title, params):

		try:

			self.printDebugMessage(u'serviceRun', u'Begin', 1)
			# Insert e-mail and title into params
			params[u'email'] = email
			if title:
				params[u'title'] = title

			requestUrl = self.baseUrl + u'/run/'
			self.printDebugMessage(u'serviceRun', u'requestUrl: ' + requestUrl, 2)

			# Get the data for the other options
			requestData = urlencode(params)

			self.printDebugMessage(u'serviceRun', u'requestData: ' + requestData, 2)
			# Errors are indicated by HTTP status codes.
			try:

				# Set the HTTP User-agent.
				user_agent = self.getUserAgent()
				http_headers = { u'User-Agent' : user_agent }
				req = Request(requestUrl, None, http_headers)
				# Make the submission (HTTP POST).

				reqH = urlopen(req, requestData.encode(encoding=u'utf_8', errors=u'strict'))
				jobId = unicode(reqH.read(), u'utf-8')
				reqH.close()

			except HTTPError as ex:

				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(str(ex), exc_type, fname, exc_tb.tb_lineno)
				os._exit(0)

			self.printDebugMessage(u'serviceRun', u'jobId: ' + jobId, 2)
			self.printDebugMessage(u'serviceRun', u'End', 1)
			return jobId

		except Exception as e:

			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			os._exit(0)

	# Get job status
	def serviceGetStatus(self, jobId):

		self.printDebugMessage(u'serviceGetStatus', u'Begin', 1)
		self.printDebugMessage(u'serviceGetStatus', u'jobId: ' + jobId, 2)
		requestUrl = self.baseUrl + u'/status/' + jobId
		self.printDebugMessage(u'serviceGetStatus', u'requestUrl: ' + requestUrl, 2)
		status = self.restRequest(requestUrl)
		self.printDebugMessage(u'serviceGetStatus', u'status: ' + str(status), 2)
		self.printDebugMessage(u'serviceGetStatus', u'End', 1)
		return status

	# Print the status of a job
	def printGetStatus(self, jobId):

		self.printDebugMessage(u'printGetStatus', u'Begin', 1)
		status = self.serviceGetStatus(jobId)
		self.printDebugMessage(u'printGetStatus', u'End', 1)


	# Get available result types for job
	def serviceGetResultTypes(self, jobId):

		self.printDebugMessage(u'serviceGetResultTypes', u'Begin', 1)
		self.printDebugMessage(u'serviceGetResultTypes', u'jobId: ' + jobId, 2)
		requestUrl = self.baseUrl + u'/resulttypes/' + jobId
		self.printDebugMessage(u'serviceGetResultTypes', u'requestUrl: ' + requestUrl, 2)
		xmlDoc = self.restRequest(requestUrl)
		doc = xmltramp.parse(xmlDoc)
		self.printDebugMessage(u'serviceGetResultTypes', u'End', 1)
		return doc[u'type':]

	# Print list of available result types for a job.
	def printGetResultTypes(self, jobId):

		self.printDebugMessage(u'printGetResultTypes', u'Begin', 1)
		resultTypeList = serviceGetResultTypes(jobId)
		for resultType in resultTypeList:
			print(resultType[u'identifier'])
			if(hasattr(resultType, u'label')):
				print(u"\t", resultType[u'label'])
			if(hasattr(resultType, u'description')):
				print(u"\t", resultType[u'description'])
			if(hasattr(resultType, u'mediaType')):
				print(u"\t", resultType[u'mediaType'])
			if(hasattr(resultType, u'fileSuffix')):
				print(u"\t", resultType[u'fileSuffix'])
		self.printDebugMessage(u'printGetResultTypes', u'End', 1)

	# Get result
	def serviceGetResult(self, jobId, type_):

		self.printDebugMessage(u'serviceGetResult', u'Begin', 1)
		self.printDebugMessage(u'serviceGetResult', u'jobId: ' + jobId, 2)
		# self.printDebugMessage(u'serviceGetResult', u'type_: ' + type_, 2)
		requestUrl = self.baseUrl + u'/result/' + jobId + u'/' + type_
		result = self.restRequest(requestUrl)
		self.printDebugMessage(u'serviceGetResult', u'End', 1)
		return result
		# https://www.ebi.ac.uk/Tools/services/rest/pfamscan/result/pfamscan-R20180725-181319-0326-39848049-p1m/out

	# Client-side poll
	def clientPoll(self, jobId):

		self.printDebugMessage(u'clientPoll', u'Begin', 1)
		result = u'PENDING'
		while result == u'RUNNING' or result == u'PENDING':
			result = self.serviceGetStatus(jobId)
			if result == u'RUNNING' or result == u'PENDING':
				time.sleep(self.checkInterval)
		self.printDebugMessage(u'clientPoll', u'End', 1)

	# Get result for a jobid
	# function modified by Mana to allow more than one output file written when 'outformat' is defined.
	def getResult(self, jobId):

		self.printDebugMessage(u'getResult', u'Begin', 1)
		self.printDebugMessage(u'getResult', u'jobId: ' + jobId, 1)
		# Check status and wait if necessary
		self.clientPoll(jobId)
		# Get available result types
		resultTypes = self.serviceGetResultTypes(jobId)

		resultData = {}
		for resultType in resultTypes:

			filename = jobId + u'.' + unicode(resultType[u'identifier']) + u'.' + unicode(resultType[u'fileSuffix'])

			if "svg" in str(resultType[u'identifier']): 
				continue

			if "png" in str(resultType[u'identifier']): 
				continue

			if "jpg" in str(resultType[u'identifier']): 
				continue

			if "jpeg" in str(resultType[u'identifier']): 
				continue

			result = self.serviceGetResult(jobId, str(resultType[u'identifier']));

			resultData[unicode(resultType[u'identifier'])] = result;

		self.printDebugMessage(u'getResult', u'End', 1)
		return resultData;


class pfam(ebi):

	"""docstring for pfam"""
	def __init__(self, debug = False):

		super().__init__()
		self.baseUrl =  u'http://www.ebi.ac.uk/Tools/services/rest/pfamscan' 
		self.debugLevel = debug
		self.setDatabase();
		self.setEvalue();

	def __str__(self):

		return "Database : " + self.database + " job_id : " + self.job_id + "\n" + self.sequence

	def setDatabase(self, database = "pfam-a"):

		if database != 'pfam-a':
			raise ValueError('Current pfram-a is the only database available')

		self.database = "pfam-a"
		return self;

	def setEvalue(self, e_value = '10'):

		evalues = ['50', '20', '10', '5', '2', '1', '0.1', '0.001', '0.0001', '1e-5', '1e-10', '1e-50', '1e-100', '1e-300']

		if e_value not in evalues:
			raise ValueError('Please select an E Value within this list', evalues);

		self.e_value = e_value
		return self

	def setSequence(self, file):

		with open(file, 'r') as myfile:
			sequence = myfile.read()

		self.sequence = sequence
		return self

	def _checkSequence(self):

		if sequence == '':
			raise ValueError('Please upload a protein sequence')

		return self

	def setJobID(self, job_id):

		self.job_id = job_id
		return self

	def submitSequence(self, email, title):

		params = {'sequence' : self.sequence, 'database' : self.database, 'evalue' : self.e_value, 'asp' : True}
		self.job_id = self.serviceRun(email, title, params)
		return self

	def retrieve(self, output = 'out'):

		result = self.getResult(self.job_id)
		if output == 'out':
			self.results =  result['out'];
		else:
			self.results = result;

	def jaccard_similarity(self, list1, list2):
		intersection = len(list(set(list1).intersection(list2)))
		union = (len(list1) + len(list2)) - intersection
		return float(intersection / union)

	def construct(self, file):

		try:

			family = {}
			unique_domains = {}
			for x in json.loads(self.results):

				name = x['seq']['name']
				unique_domains[x['acc']] = x['acc']

				if name in family:

					family[name].update( 
						{len(family[name]) : {'to' : x['seq']['to'], 'from' : x['seq']['from'], 'type' : x['type'], 'fname' : x['name'], 'desc' : x['desc'], 'domain' : x['acc'] } 
					} )

				else:

					family.update({ name : 
						{0 : {'to' : x['seq']['to'], 'from' : x['seq']['from'], 'type' : x['type'], 'fname' : x['name'], 'desc' : x['desc'], 'domain' : x['acc'] } 
					}})


			for key, value in family.items():

				domains = ''
				for key2, value2 in value.items():

					if domains == '':

						domains = value2['domain']

					else:

						domains = domains + "," + value2['domain']

				family[key].update({'domains' : domains})

			with open(file, 'r') as myfile:

				sequences = json.load(myfile)
				sequences['pfam'] = {'job_id' : self.job_id, 'unique_domains' : unique_domains};

				for key, value in family.items():

					if key in sequences['sequences']:
						sequences['sequences'][key]['pfam'] = value;

			x = 0
			for key, value in sequences['sequences'].items():


				if x == 0:

					query_sequence = set(value['pfam']['domains'].split(','));
					score = 1;

				else : 

					subject_sequence = set(value['pfam']['domains'].split(','));
					score = self.jaccard_similarity(query_sequence, subject_sequence)

				sequences['sequences'][key]['pfam']['jaccard_similarity'] = score;

				x += 1;
				pass

			return sequences

		except Exception as e:

			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(e, '\n', exc_type, fname, exc_tb.tb_lineno)
			os._exit(0)


class blast(ebi):

	"""docstring for pfam"""
	def __init__(self, debug = False):

		super().__init__()
		self.baseUrl =  u'http://www.ebi.ac.uk/Tools/services/rest/psiblast'
		self.debugLevel = debug
		self.alignments = 20
		self.setDatabase()

	def __str__(self):

		return "Database : " + self.database + " job_id : " + self.job_id + "\n" + self.sequence

	def setDatabase(self, database = "uniprotkb"):

		if database != 'uniprotkb':
			raise ValueError('Current pfram-a is the only database available')

		self.database = "uniprotkb"
		return self;

	def setSequence(self, sequence):

		self.sequence = sequence
		return self

	def _checkSequence(self):

		if sequence == '':
			raise ValueError('Please upload a protein sequence')

		return self

	def setJobID(self, job_id):

		self.job_id = job_id
		return self

	def submitSequence(self, email, title):

		params = {'sequence' : self.sequence, 'database' : self.database, 'alignments' : self.alignments}
		self.job_id = self.serviceRun(email, title, params)
		return self

	def retrieve(self):

		return self.getResult(self.job_id)


