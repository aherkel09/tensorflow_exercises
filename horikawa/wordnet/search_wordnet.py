from nltk.corpus import wordnet as wn

def search_wordnet(offset):  
    synset = wn.synset_from_pos_and_offset('n', int(offset))
    lemma = synset.lemmas()[0]
    definition = synset.definition()
    
    return (lemma, definition)


if __name__ == '__main__':
    print(search_wordnet(3950228))