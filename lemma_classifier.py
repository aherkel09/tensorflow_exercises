import codecs, csv, os

class LemmaClassifier:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.lemma_files = self.get_lemma_files()

    def get_lemma_files(self):
        file_tree = {}
        for subdir, dirs, files in os.walk(self.root_directory + '\\wordnet'): # check all files in all subdirectories
            for filename in files:
                if filename.startswith('lemmas'):
                    run = filename.split('-')[1].replace('.tsv', '')
                    file_tree[run] = os.path.join(subdir, filename)

        return file_tree

    def get_lemmas(self):
        lemmas = {}
        for run, file in self.lemma_files.items():
            run_lemmas = []
            with open(file, 'rb') as tsv:
                reader = csv.reader(codecs.iterdecode(tsv, 'utf-8'), delimiter='\t')
                for row in reader:
                    run_lemmas.append(row)

            lemmas[run] = run_lemmas

        return lemmas

    def classify_lemmas(self, lemmas):
        categories = {}
        for run in lemmas:
            print('\nRun' + run)
            run_categories = []
            for row in lemmas[run]:
                row_categories = self.ask_category(row)
                run_categories.append(row_categories)

            categories[run] = run_categories
        
        return categories

    def ask_category(self, row):
        categories = []
        for lemma in row:
            category = input('Is ' + lemma + ' living or nonliving? (1/2): ')
            if category == '1' or category == '2':
                categories.append(int(category))

        return categories

    def drop_duplicate_runs(self, categories):
        duplicates = []
        run_list = []
        for run in categories:
            if categories[run] not in run_list:
                run_list.append(categories[run])
            else:
                duplicates.append(run)

        for run in duplicates:
            categories.pop(run)
            
        return categories

    def drop_duplicate_rows(self, categories):
        for run in categories:
            row_list = []
            
            for row in categories[run]:
                if row not in row_list:
                    row_list.append(row)
                else:
                    row = []
            
        return categories

    def write_categories(self, categories):
        for run in categories:
            with open('living_nonliving-' + run, 'a') as tsv:
                writer = csv.writer(tsv, delimiter='\t')
                writer.writerows(categories[run])

    def decode_categories(self, lemmas, categories):
        for run in categories:
            print('\nRun ' + run + '\n')
            
            for row in range(len(categories[run])):
                row_list = []
                
                for category in range(len(categories[run][row])):
                    if categories[run][row][category] == 1:
                        print(lemmas[run][row][category], '==> living')
                    elif categories[run][row][category] == 2:
                        print(lemmas[run][row][category], '==> nonliving')
                
def request_action(lemmas, categories):
    print('\n1: view the categories of all classified lemmas')
    print('2: write all classified lemmas to .tsv files')
    print('exit: exit')
    action = input('enter the identifier of the action you wish to perform: ')

    if action == '1':
        classifier.decode_categories(lemmas, categories)
    elif action == '2':
        classifier.write_categories(categories)
    elif action == 'exit':
        return
    else:
        print('error: please enter a valid selection')
        
    return request_action(lemmas, categories)
        
if __name__ == '__main__':
    classifier = LemmaClassifier()
    lemmas = classifier.get_lemmas()
    categories = classifier.classify_lemmas(lemmas)
    categories = classifier.drop_duplicate_runs(categories)
    categories = classifier.drop_duplicate_rows(categories)

    request_action(lemmas, categories)
