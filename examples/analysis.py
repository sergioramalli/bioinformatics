import json, os, csv
from config import config, system_config, output_files
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



with open(output_files['kmeans_model_2'], 'rb') as f:
	km = pickle.load(f)

val = km.labels_

print(val);

# num = 0
# for x in val:

# 	# print(x);
# 	num += 1
# 	if num > 400:
# 		break;
# 	pass



# plt.scatter(data[:,0],data[:,1], label='True Position')

# for x in data:

# 	predict_me = np.array(x)
# 	predict_me = predict_me.reshape(-1, len(predict_me))
# 	prediction = km.predict(predict_me)
# 	print(prediction, x)
# 	break;
# 	pass

# I need orignal query. -> fasta file 
# I need blast query which includes query sequence. -> fasta file. 
# I need json file with the pfam domains, blast scores and cog id. -> this becomes the main file. 
# I need the CSV file with the distance scores. 

# Then i need to find which cluster my orignal query belongs in

# note also only looking at top domain hits, and not taking into account gaps


# query (actinobacteria) -> psi-blast -> pfam_construct -> get cogs -> process -> scoring function -> cluster analysis -> annotate

# psi_blast json file. <-- arrives from psi blast output and modifies files. 
# then outputs to json file. 

# Next steps do same process in psi-blast file
# Next steps do same process in pfam file. 

# installer to install all packages. 