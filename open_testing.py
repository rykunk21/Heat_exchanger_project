import csv

with open('Pipe_Sizes.csv', 'r') as fp:
    lines = csv.reader(fp)

    for line in lines:
        if line == '':
            continue
        else:
            print(line)

