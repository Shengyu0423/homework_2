import sys
import csv

# Check the number of arguments
if len(sys.argv) < 4:
    print("Usage: reader.py <src> <dst> <change1> <change2> ...")
    sys.exit(1)

# Read changes from cmd
in_csv = sys.argv[1]
out_csv = sys.argv[2] 
change_values = sys.argv[3:]

# Reading the original data from in.csv file
with open('in.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

# Applying changes
for change in change_values:
    change_parts = change.split(',')
    if len(change_parts) != 3:
        print(f"Invalid change format: {change}. Correct format: x, y, new_value")
        continue

    try:
        x, y, new_value = change_parts
        x, y = int(x), int(y)
        if x < 0 or y < 0 or y >= len(data) or x >= len(data[0]):
            print(f"Change {change} is out of range.")
            continue
        data[y][x] = new_value
    except ValueError:
        print(f"Invalid change format: {change}. Correct format: x, y,new_value")

# Writing the change into out.csv file
with open('out.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Reading the change from out.csv file
with open('out.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

