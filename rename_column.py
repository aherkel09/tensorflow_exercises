import os, csv, shutil

def get_par_files():
    filepaths = []
    root_dir = os.getcwd()
    
    for dirpath, subdirs, files in os.walk(root_dir):
        for filename in files:
            if filename.startswith('horikawa.par'):
                path = os.path.join(dirpath, filename)
                filepaths.append(path)
                
    return filepaths

def read_file_data(file):
    headers = []
    data = []
    
    with open(file, 'r') as par:
        reader = csv.reader(par, delimiter='\t')
        headers = next(reader)
        
        for row in reader:
            data.append(row)
    
    return headers, data
    
def write_file_data(file, headers, data):
    with open(file, 'w') as par:
        writer = csv.writer(par, delimiter='\t')
        writer.writerow(headers)
        writer.writerows(data)

def rename_column(headers):
    print('Original:', headers)
    headers = ['Cumulative_Onset' for h in headers if h == 'Cululative_Onset']
    print('Corrected:', headers)
    
    return headers

if __name__ == '__main__':
    files = get_par_files()
    
    for file in files:
        headers, data = read_file_data(file)
        headers = rename_column(headers)
        write_file_data(file, headers, data)
        
    
