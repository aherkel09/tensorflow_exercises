import codecs, csv, os
from pathlib import Path

# FIXME: create file in proper location for all runs & subjects
def write_to_file(run_data):
    with open('horikawa.par', 'w', newline='') as par:
        writer = csv.writer(par, delimiter='\t')
        writer.writerow(run_data.keys()) # headers
        num_rows = len(run_data['Duration']) # get list length from arbitrary column

        row = 0
        while row < num_rows:
            row_data = []
            for data in run_data:
                row_data.append(run_data[data][row])
                
            writer.writerow(row_data)
            row += 1

def get_tsv_data():
    data = {}
    
    run = 1
    while run <= 20:
        data[run] = get_run_data(run)
        run += 1
        
    return data

def get_run_data(run):
    root_directory = os.getcwd() + '\\tsv_out'
    category_file = os.path.join(root_directory, 'living_nonliving-' + str(run) + '.tsv')

    unique_rows = 3 # number of unique rows of data in living_nonliving files
    run_data = {
        'Cululative_Onset': [[(36 + 24*n) for n in range(0,25)]]*unique_rows, # onsets per tsv data
        'Condition_Number_Code': get_codes(category_file),
        'Duration': [[15 for d in range(0,25)]]*unique_rows, # durations per tsv data
        'Weight': [[1 for w in range(0, 25)]]*unique_rows, # set all weights to 1
    }
    
    return run_data

def get_codes(file):
    # get living_nonliving codes from file
    codes = []
    with open(file, 'rb') as tsv:
        reader = csv.reader(codecs.iterdecode(tsv, 'utf-8'), delimiter='\t')
        for row in reader:
            codes.append(row)
                    
    return codes

if __name__ == '__main__':
    print(get_tsv_data())
