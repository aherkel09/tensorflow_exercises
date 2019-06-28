from nltk.corpus import wordnet as wn

id_list = [2690373, 1976957, 4210120] # get all from .tsv files

for i in id_list:
    synset = wn.synset_from_pos_and_offset('n', i)
    print(synset.lemmas()[0].name())
