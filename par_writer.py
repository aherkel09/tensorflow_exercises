import codecs, csv, os

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
        
    return data

def get_run_data(run):
    root_directory = os.getcwd() + '\\tsv_out\\'
    run_data = {}
    
    # map column names to .tsv filenames
    filename_map = {
        'Cumulative_Onset': 'onset',
        'Condition_Number_Code': 'living_nonliving',
        'Duration': 'duration',
    }
    
    for fname in filename_map:
        in_file = root_directory + filename_map[fname] + '-' + run + '.tsv'
        file_data = []
        
        with open(in_file, 'rb') as tsv:
            reader = csv.reader(codecs.iterdecode(tsv, 'utf-8'), delimter='\t')
            for row in reader:
                file_data.append(row)
        
        run_data[fname] = file_data
        
    return run_data

if __name__ == '__main__':
    print(get_tsv_data())
