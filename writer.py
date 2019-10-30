import csv

class Writer:
    def write_to_file(self, filename, headers, data):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            
            for h in headers:
                writer.writerow(h)
                
            for d in data:
                writer.writerow(d)
