import csv
from tsv_reader import TSVReader
from tsv_writer import TSVWriter

def compare_headers(reader, file_tree):
    print('Comparing column headers...')
    match = None
    for subdir, file_list in file_tree.items():
        for f in file_list:
            headers = reader.get_column_headers(f)
            if not match:
                match = headers
            elif headers != match:
                raise ValueError('Headers do not match.')
            
    print('All headers match.')
    return match

def write_all_columns(reader, file_tree, headers):
    for subdir, file_list in file_tree.items():
        for f in file_list:
            run = f.split('-')[1][:2]
            for h in headers:
                writer = TSVWriter(h + '-' + str(int(run)) + '.tsv')
                col_num = reader.get_column_number(headers, h)
                col_data = reader.read_column_data(f, col_num)
                writer.write_column_data(h, col_data)

def compare_all_data(headers):
    run = 1
    
    while run <= 20:
        unmatched = [True for h in headers]
        
        for h in range(len(headers)):
            prev_row = None
            filestring = 'tsv_out\\' + headers[h] + '-' + str(run) + '.tsv'
            with open(filestring, 'r') as tsv:
                reader = csv.reader(tsv, delimiter='\t')

                row_count = 0
                for row in reader:
                    if not prev_row:
                        prev_row = row
                    elif row_count % 2 == 0 and row != prev_row:
                        unmatched[h] = headers[h]
                    row_count += 1

        print('Unmatched columns in run ' + str(run) + ':', [u for u in unmatched if u != True])
        run += 1
        
if __name__ == '__main__':
    reader = TSVReader()
    tsv_files = reader.get_files()
    matched_headers = compare_headers(reader, tsv_files)
    
    if matched_headers:
        write_all_columns(reader, tsv_files, matched_headers)
        compare_all_data(matched_headers)
        
