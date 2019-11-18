import csv, os

def compare(files):
    checked = {}
    matched_files = []
    
    for f in files:
        data = read_file(f)
        
        for key, val in checked.items():
            if val == data:
                matched_files += [(key, f)]
                
        checked[f] = data
                
    
    return matched_files

def read_file(fname):
    with open(fname, 'r') as par:
        reader = csv.reader(par, delimiter='\t')
        return list(reader)

if __name__ == '__main__':
    par_files = []
    
    for path, subdir, files in os.walk(os.getcwd()):
        for name in files:
            if name.endswith('.par'):
                par_files += [name]
    
    
    matches = compare(par_files)
    
    for m in matches:
        print(m)
    
    print(len(matches), 'total matches')
        