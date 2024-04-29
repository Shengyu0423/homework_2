import sys
import csv
import json
import pickle
import os


class DataProcessor:
    def __init__(self, in_file, out_file, change_values):
        self.in_file = in_file
        self.out_file = out_file
        self.change_values = change_values

    def read_data(self, file_name):
        _, file_extension = os.path.splitext(file_name)
        file_extension = file_extension.lower()
        if file_extension == '.csv':
            with open(file_name, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                return data
        elif file_extension == '.json':
            with open(file_name, 'r') as file:
                return json.load(file)
        elif file_extension == '.pickle':
            with open(file_name, 'rb') as file:
                return pickle.load(file)
        else:
            print(f"Unsupported file format: {file_extension}")
            sys.exit(1)

    def write_data(self, file_name, data):
        _, file_extension = os.path.splitext(file_name)
        file_extension = file_extension.lower()
        if file_extension == '.csv':
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        elif file_extension == '.json':
            with open(file_name, 'w') as file:
                json.dump(data, file)
        elif file_extension == '.pickle':
            with open(file_name, 'wb') as file:
                pickle.dump(data, file)
        else:
            print(f"Unsupported file format: {file_extension}")
            sys.exit(1)

    def process_changes(self):
        # Reading the original data
        data = self.read_data(self.in_file)

        # Applying changes
        for change in self.change_values:
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

        # Writing the changes into the destination file
        self.write_data(self.out_file, data)

        # Reading the changes from the destination file and printing them
        print("Changes written to the destination file: ")
        print("-------------------------------------------")
        if self.out_file.endswith('.csv'):
            with open(self.out_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
        elif self.out_file.endswith('.json'):
            with open(self.out_file, 'r') as file:
                data = json.load(file)
                print(data)
        elif self.out_file.endswith('.pickle'):
            with open(self.out_file, 'rb') as file:
                data = pickle.load(file)
                print(data)
        else:
            print(f"Unsupported file format: {self.out_file}")


# Check the number of arguments
if len(sys.argv) < 4:
    print("Usage: reader.py <src> <dst> <change1> <change2> ...")
    sys.exit(1)

in_file = sys.argv[1]
out_file = sys.argv[2]
change_values = sys.argv[3:]

# Create a DataProcessor instance and process changes
processor = DataProcessor(in_file, out_file, change_values)
processor.process_changes()


