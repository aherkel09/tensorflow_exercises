import csv

with open ('abcd_data/fastqc01.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)

print(headers)