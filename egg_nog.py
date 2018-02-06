import requests
from Bio import SeqIO

class eggNogRestCall(object):

    def call(self, id = "ENOG410ZSWV"):

        url = "http://eggnogapi.embl.de/nog_data/json/tree,trimmed_alg/" + id;
        return requests.post(url).json();

    pass

eggRest = eggNogRestCall();
result = eggRest.call('ENOG410ZSWV');

tree = result['tree']
raw_alg = eggRest.read_fasta(result['raw_alg']);