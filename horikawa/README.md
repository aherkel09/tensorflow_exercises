* `wordnet_reader.py` searches subdirectories for tsv files & gets the wordnet offsets (numerical identifier for a word) from the 'category_id' column of each file. It then uses the wordnet interface to retrieve each word's 'lemma' (the actual word, e.g. 'bat', 'swan', &c.) & finally, writes the offsets, lemmas & definitions to a .csv file ( a modified version can be found in `offsets/imagery_offsets.csv`)

* `wordnet_by_run.py` searches .tsv files for each run (I believe there are 20 runs of imagery data per subject) & creates a separate file for the lemmas in each run (e.g. the wordnet offsets from run 1 are mapped to lemmas in `tsv_out/lemmas-1.tsv`)

* `lemma_classifier.py` goes through the lemma files for each run & asks the user to classify lemmas as living or nonliving. The user can then write these out (results in `tsv_out/living_nonliving-XX.tsv`), or view a list of their inputs.

* `offsets/imagery_offsets.csv` & `offsets/perception_offsets.csv` contain the output from wordnet_reader.py, i.e. all the unique lemmas from all the imagery & perception runs. The versions attached also have living_nonliving columns (1 --> living, 2 --> nonliving) & a count of the lemmas in each category. Running `offsets/compare_offsets.py` shows that the imagery & perception lemmas are identical (i.e. subjects were asked to imagine the same objects they were presented).

* `data_selector.py` creates shuffled datasets from `offsets/perception_offsets/csv` & selects random pairs of living & nonliving items. **TODO:** This data should be formatted & written out so that it can be used as input to classifier models.
