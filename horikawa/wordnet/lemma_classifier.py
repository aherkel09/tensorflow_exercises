import codecs, csv, os

class LemmaClassifier:
    def __init__(self, lemmas):
        self.root_directory = os.getcwd()
        self.lemmas = lemmas
        self.classified = self.classify_lemmas()
        self.write_categories()

    def classify_lemmas(self):
        classified = {}
        for run in self.lemmas:
            print('\nClassifying Run ' + run + '...')
                        
            for lemma in self.lemmas[run]:
                if lemma not in classified.keys():
                    category = self.ask_category(lemma)
                    classified[lemma] = category
                else:
                    category = classified[lemma]
                                                    
        return classified

    def ask_category(self, lemma):
        category = input('Is ' + lemma + ' living or nonliving? (1/2): ')
        
        try:
            if category == '1' or category == '2':
                return int(category)
            else:
                raise Exception
        except:
            self.showError()
            return self.ask_category(lemma)
    
    def showError(self):
        print('Error: please enter a valid category.')

    def write_categories(self):
        run_count = 1
        for run in self.lemmas:
            run_lemmas = [self.classified[l] for l in self.lemmas[run]]
            
            with open('offsets\\training_offsets.csv', 'w', newline='\n') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(['living_nonliving'])
                [writer.writerow([l]) for l in run_lemmas]
            
            run_count += 1