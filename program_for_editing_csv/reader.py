import sys
import csv

# Check the number of arguments
if len(sys.argv) < 4:
    print("Usage: reader.py <src> <dst> <change1> <change2> ...")
    sys.exit(1)

# Read changes from cmd
in_csv = sys.argv[1]
out_csv = sys.argv[2] 
change_values = sys.argv[3].split(',') 

x, y, new_value = int(change_values[0]), int(change_values[1]), change_values[2]

# Reading the original data from in.csv file
with open('in.csv', 'r', newline='') as infile:
    reader = csv.reader(infile)
    data = list(reader)


data[y][x] = new_value

# Writing the change into out.csv file
with open('out.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)

# Reading the change from out.csv file
with open('out.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

