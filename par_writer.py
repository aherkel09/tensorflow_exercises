import codecs, csv, os
from pathlib import Path

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

def get_output_files(data):
    files = {}
    
    for run in data:
        files[run] = get_run_files(run)

    return files

def get_run_files(run):
    files = []
    
    # format run for file output
    if run < 10:
        run = '00' + str(run)
    else:
        run = '0' + str(run)

    # map data rows to subjects (based on tsv_in data)
    rows_to_subjects = {
        1: ['1', '2', '3'],
        2: ['4'],
        3: ['5']
    }
    
    for row in rows_to_subjects:
        for subject in rows_to_subjects[row]:
            filename = 'FS_0' + subject + '\\bold\\' + run + '\\horikawa.par'
            filepath = os.path.join(os.getcwd(), filename)
            files.append(filepath)
            
    return files

# FIXME: function writing 3 rows of lists instead of 25 rows of values
def write_by_run(data, files):
    for run in data:
        for file in files[run]:
            with open(file, 'w', newline='') as par:
                writer = csv.writer(par, delimiter='\t')
                writer.writerow(data[run].keys()) # headers

                col = 0
                num_cols = len(data[run]['Duration']) # get list length from arbitrary column
                while col < num_cols:
                    col_data = []
                    for r in data[run]:
                        # get column data for subject & run
                        col_data.append(data[run][r][col])

                    writer.writerow(col_data)
                    col += 1

if __name__ == '__main__':
    data = get_tsv_data()
    files = get_output_files(data)
    write_by_run(data, files)
