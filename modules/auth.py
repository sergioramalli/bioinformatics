import math, operator, os

class process(object):

	highest_score = 0.0;

	def __init__(self):
		pass;

	def processData(self, data):

		# data = self.normalize_dict(data)
		x = 0;
		remove = {}
		for key, value in data.items():

			if not 'pfam' in value:
				remove[key] = key
				continue;

			if 'sequence' in value['pfam']:
				data[key]['sequence'] = value['pfam']['sequence'];
				data[key]['pfam'].pop('sequence')
				data[key]['blast'].pop('sequence')
				data[key]['pfam']['domains'] = len(value['pfam']['info'])

			data[key]['key'] = x;
			x += 1
		
		for key, value in remove.items():
			data.pop(key)

		return data;

	def normalize_dict(self, data):

		allscores = {}
		for key, value in data.items():

			ss = 0
			for key2, value2 in value['pfam']['info'].items():

				ss =+ value2['score']
				pass

			allscores[key] = (ss / len(value['pfam']['info']));
			pass

		max_val = max(allscores.iteritems(), key=operator.itemgetter(1))[1]
		min_val = min(allscores.iteritems(), key=operator.itemgetter(1))[1]
		delta = max_val - min_val

		scores = {}
		for key, d in allscores.items():
			scores[key] = {'norm_score' : ((d - min_val)/delta), 'avg_score' : d}

		for key, value in scores.items():

			data[key]['pfam']['scores'] = value;
			pass

		return data;

	def getMaxDomain(self, data):
		return max(int(d['pfam']['domains']) for d in data.values())

	def getMinDomain(self, data):
		return min(int(d['pfam']['domains']) for d in data.values())

	def domain_creator(self, obj):

		domain = [];
		for key, value in obj.items():
			domain.append(key)

		return domain;

	def jaccard_similarity(self, list1, list2):

	    intersection = len(list(set(list1).intersection(list2)))
	    union = (len(list1) + len(list2)) - intersection

	    if union == 0:
	    	return intersection;

	    return float(float(intersection) / float(union))

	def js_score(self, domains1, domains2, maxDomains):

		return self.jaccard_similarity(self.domain_creator(domains1['info']), self.domain_creator(domains2['info']));

	def cogs(self, query, hit):

		if query['cog_id'] == hit['cog_id']:

			return 1

		return 0

	def domain_similarity(self, domains1, domains2, maxDomains):

		js = self.jaccard_similarity(self.domain_creator(domains1['info']), self.domain_creator(domains2['info']));
		domList = list(set(self.domain_creator(domains1['info'])).intersection(self.domain_creator(domains2['info'])))

		d_score = 0.0;
		for pfam_id in domList:

			domain1_score = domains1['info'][pfam_id]['n_norm_score']
			domain2_score = domains2['info'][pfam_id]['n_norm_score']
			d_score += (domain1_score + domain2_score) / 2.0;
			pass	

		if len(domList) > 0:

			score = js + ( ( 0.5 / float(maxDomains)) * (d_score / float(len(domList))) ) 

		else:

			score = js;

		if score > self.highest_score:
			self.highest_score = score; 


		return score;


