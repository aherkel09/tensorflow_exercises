import csv, math, os

def find_files(root):
    filenames = []
    for subdir, dirs, files in os.walk(root): # check all files in all subdirectories
                for file in [f for f in files if f.endswith('.tsv')]: # search .tsv files only
                    filepath = os.path.join(subdir, file)
                    filenames.append(filepath)
    
    return filenames

def read_file(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return list(reader)

def get_column(headers, col_name):
    return headers.index(col_name)

def convert(data, col):
    for d in data:
        d[col] = d[col].split('.')[0]
        
    return data

def write_file(filepath, data):
    with open(filepath, 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)
        
if __name__ == '__main__':
    files = find_files('C:\\Users\\aherk\\ccn_scripts\\horikawa\\perceptionTraining')
    for f in files:
        data = read_file(f)
        column = get_column(data[0], 'stim_id')
        converted = convert(data, column)
        write_file(f, converted)