def save_data_to_file(inventory, filename):
    try:
        with open(filename, 'w') as file:
            file.write(str(inventory))
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def load_data_from_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            data = eval(content)
        print("Data loaded successfully!")
        return data
    except Exception as e:
        print(f"Error loading data from file: {e}")
        return {}


