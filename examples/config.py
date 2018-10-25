import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]) + '/modules/')

config = {

	'threads' : 12,
	'iterations' : 1,

	'subject_sequences' : "../genomes/actinobacteria.faa",
	'subject_db' : "../genomes/blast_db/actinobacteria",

	'query_sequences' : "/home/turingrepublic/Desktop/Thesis_/final/queries/WP_011274277_1.faa",
	# 'query_sequences' : '../queries/NP_414543_1_longer_than_subjects.faa',

	# for examples only
	'psi_results' : '../results/actinobacteria/psi_example',
	'psi_results_fasta' : '../results/actinobacteria/psi_example.fasta',

	# pfam domains results example
	'pfam_domains' : '../results/actinobacteria/pfam_domains_example.json',
	# pfam matched domains example
	'pfam_processed_domains' : '../results/actinobacteria/pfam_processed_domains_example.json',

	# for examples only 
	'pfam_job_id' : 'pfamscan-R20180829-093008-0418-40011235-p1m'

}
