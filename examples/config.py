import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]) + '/modules/')

config = {
		
	# unique identify for the job 
	# 'job_name' : 'NP_414543_1_90_hits',
	'job_name' : '9_90',

	# 'query' : "/home/turingrepublic/Desktop/Thesis_/final/queries/WP_011274277_1.faa",
	# 'query' : '../queries/A0A2D5C7R1_9ACTN.fasta',
	# 'query' : '../queries/NP_414543_1_longer_than_subjects.faa',
	'query' : '../queries/9actn.fasta',

	# the name of the output file. 
	'result_directory' : 'results/',

	# whether or not to use an exisiting blast db in psi-blast analysis 
	'from_existing_db' : True,

	# whether or not to use an exisiting cogs db in cogs analysis 
	'create_cogs_db' : False,

	#how many computer threads to use for analysis  
	'threads' : 12,

	# how many iterations to use in psi-blast. 
	'iterations' : 2,

	# how many hits you want back from psi-blast
	'hits' : 90

}

system_config = {
	
	# Subject sequences to use for psi-blast analysis. @todo make it so cogs db is set from same config item
	'subject_sequences' : "../genomes/actinobacteria.faa",

	# the subject db made from subject sequences needed if from_exisiting_db is set to true.
	'subject_db' : "../genomes/blast_db/actinobacteria", 

	'cogs_fasta' : '../genomes/cogs.fa', 

	'cogs_p2o' : '../genomes/cogs.p2o.csv', 

	'cogs_genomes_cogs' : '../genomes/COGs'

}

# temp files used internally by the code. 
output_files = {}

# Where the blast results are kept 
output_files['blast'] = config['result_directory'] + config['job_name'] + '/' + 'blast/'
output_files['blast_fasta'] = output_files['blast'] + config['job_name'] + '.fasta'
output_files['blast_json'] = output_files['blast'] + config['job_name'] + '.json'
output_files['blast_csv'] = output_files['blast'] + config['job_name'] + '.csv'

output_files['interscan'] = config['result_directory'] + config['job_name'] + '/' + 'interscan/'
output_files['interscan_pfam'] = output_files['interscan'] + config['job_name'] + '_pfam'
output_files['interscan_pfam_json'] = output_files['interscan'] + config['job_name'] + '_pfam.json'

output_files['cogs'] = config['result_directory'] + config['job_name'] + '/' + 'cogs/'
output_files['cogs_csv'] = output_files['cogs'] + config['job_name'] + '.csv'
output_files['cogs_json'] = output_files['cogs'] + config['job_name'] + '.json'

output_files['final'] = config['result_directory'] + config['job_name'] + '/final.json'
output_files['analysis'] = config['result_directory'] + config['job_name'] + '/analysis.json'
output_files['distant_full_csv'] = config['result_directory'] + config['job_name'] + '/distance_full.csv'
output_files['distant_score_csv'] = config['result_directory'] + config['job_name'] + '/distance_score.csv'
output_files['distant_score_csv_2'] = config['result_directory'] + config['job_name'] + '/distance_score_2.csv'
output_files['distant_cluster_csv'] = config['result_directory'] + config['job_name'] + '/distance_cluster.csv'

output_files['kmeans_model'] = config['result_directory'] + config['job_name'] + '/kmeans.pickle'
output_files['kmeans_model_2'] = config['result_directory'] + config['job_name'] + '/kmeans_2.pickle'
