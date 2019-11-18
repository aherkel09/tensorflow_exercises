import csv, os

def split_data(file):
    file_data = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        file_data += next(reader)
        for row in reader:
            row[4] = row[4].split('.')[0]
            file_data += [row]

    return file_data

def get_tsv_files():
    tsv = []
    for path, subdirs, files in os.walk('perceptionTest'):
            for name in files:
                if name.endswith('.tsv'):
                    tsv += [os.path.join(path, name)]

    return tsv

def overwrite(files):
    for file in files:
        data = split_data(file)
        
        with open(file, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)

if __name__ == '__main__':
    files = get_tsv_files()
    overwrite(files)
