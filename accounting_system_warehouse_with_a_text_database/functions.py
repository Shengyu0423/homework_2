def save_balance_to_file(balance, filename):
    try:
        with open(filename, 'w') as file:
            file.write(str(balance))
        print("Account balance saved successfully!")
    except Exception as e:
        print(f"Error saving account balance: {e}")

def save_inventory_to_file(inventory, filename):
    try:
        with open(filename, 'w') as file:
            for product, details in inventory.items():
                file.write(f"Product name: {product}, Price: {details['price']}, Quantities: {details['quantities']}\n")
        print("Warehouse inventory saved successfully!")
    except Exception as e:
        print(f"Error saving warehouse inventory: {e}")

def save_operations_to_file(operations, filename):
    try:
        with open(filename, 'w') as file:
            for operation in operations:
                operation_type, product_name, price, quantity = operation
                file.write(f"Type: {operation_type}, Product Name: {product_name}, Price: {price}, Quantities: {quantity}\n")
        print("Recorded operations saved successfully!")
    except Exception as e:
        print(f"Error saving recorded operations: {e}")

def load_original_warehouse_inventory(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            original_warehouse_inventory = eval(content)
        print("warehouse inventory successfully!")
        return original_warehouse_inventory
    except Exception as e:
        print(f"Error loading warehouse inventory: {e}")
        return {}
