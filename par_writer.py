import codecs, csv, os

def write_to_file(data):
    with open('horikawa.par', 'w', newline='') as par:
        writer = csv.writer(par, delimiter='\t')
        writer.writerow(data.keys()) # headers
        num_rows = len(data['Duration']) # get list length from arbitrary column

        row = 0
        while row < num_rows:
            row_data = []
            for d in data:
                row_data.append(data[d][row])
                
            writer.writerow(row_data)
            row += 1

if __name__ == '__main__':
    # sample data. real dict should be built from tsv files.
    data = {
        'Cumulative_Onset': [1, 2, 3],
        'Condition_Number_Code': [1, 2, 2],
        'Duration': [1, 1, 1],
        'Weight': [1, 1, 1],
    }
    write_to_file(data)
