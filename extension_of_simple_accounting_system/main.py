from functions import load_data_from_file, save_data_to_file
from manager import Manager

account_balance = 1000
recorded_operations = []
warehouse_inventory = {}

# Create an instance of Manager
manager = Manager()

@manager.assign("balance")
def balance(manager):
    global account_balance
    try:
        amount = float(input("\nPlease add or subtract the amount to the account: "))
        account_balance += amount
        print(f"\nUpdated account balance: {account_balance}")
    except ValueError:
        print("\nError: Please enter a valid amount.")

@manager.assign("sale")
def sale(manager):
    global account_balance
    try:
        product_name = input("\nPlease enter the product name: ")
        if product_name in warehouse_inventory:
            price = float(input("\nPlease enter the price per unit: "))
            quantity = int(input("\nPlease enter the quantity sold: "))

            if warehouse_inventory[product_name]["quantities"] >= quantity:
                total_sale_amount = price * quantity
                account_balance += total_sale_amount
                
                # Update the warehouse inventory
                warehouse_inventory[product_name]["quantities"] -= quantity
                print("\nSale completed successfully!")
                
                # Record the operation
                recorded_operations.append(("sale", product_name, price, quantity))
            else:
                print("\nError: Insufficient inventory for sale!")
        else:
            print("\nError: Invalid product name!")
    except ValueError:
        print("\nPlease enter a valid input for product name, price, and quantity.")

@manager.assign("purchase")
def purchase(manager):
    global account_balance
    try:
        product_name = input("\nPlease enter the product name: ")
        if product_name in warehouse_inventory:
            price = float(input("\nPlease enter the price per unit: "))
            quantity = int(input("\nPlease enter the quantity to purchase: "))

            if quantity > 0:
                total_purchase_cost = price * quantity
                if account_balance >= total_purchase_cost:
                    # Update account balance
                    account_balance -= total_purchase_cost

                    # Update warehouse inventory
                    warehouse_inventory[product_name]["quantities"] += quantity
                    print("\nPurchase completed successfully!")

                    # Record the operation
                    recorded_operations.append(("purchase", product_name, price, quantity))
                else:
                    print("\nError: Insufficient account balance for purchase!")
            else:
                print("\nError: Invalid quantity for purchase!")
        else:
            # Ask user to provide details of new product
            print("\nProduct not found in inventory. Please provide the following information:")
            price = float(input("\nEnter the price per unit: "))
            quantity = int(input("\nEnter the initial quantity: "))

            if quantity > 0:
                total_purchase_cost = price * quantity
                if account_balance >= total_purchase_cost:
                    # Update account balance
                    account_balance -= total_purchase_cost

                    # Add new product to inventory
                    warehouse_inventory[product_name] = {"price": price, "quantities": quantity}
                    print("\nNew product added to inventory successfully!")
                    
                    # Record the operation
                    recorded_operations.append(("purchase", product_name, price, quantity))
                else:
                    print("\nError: Insufficient account balance for purchase!")
            else:
                print("\nError: Inalid quantity for purchase!")

    except ValueError:
        print("\nError: Please enter valid inputs for price and quantity. ")

@manager.assign("account")
def account(manager):
    global account_balance
    print(f"\nCurrent account balance: {account_balance}")

@manager.assign("list")
def list(manager):
    print("\nWarehouse Inventory:\n ")
    for item, details in warehouse_inventory.items():
        print(f"{item.capitalize()}:")
    for detail, value in details.items():
        print(f"- {detail.capitalize()}: {value}")

@manager.assign("warehouse")
def warehouse(manager):
    product_name = input("\nPlease enter one of the products to check details: ")
    if product_name in warehouse_inventory:
        print(f"\nProduct: {product_name.capitalize()}")
        for detail, value in warehouse_inventory[product_name].items():
            print(f"- {detail.capitalize()}: {value}")
    else:
        print("\nError: Product not found in warehouse! ")

@manager.assign("review")
def review(manager):
    try:
        from_index = input("\nEnter the 'starting' index: ")
        to_index = input("\nEnter the 'end' index: ")

        if from_index == "":
            from_index = 1
        else:
            from_index = int(from_index)

        if to_index == "":
            to_index = len(recorded_operations)
        else:
            to_index = int(to_index)

        if from_index < 1 or to_index > len(recorded_operations) or from_index > to_index:
            print("\nError: Invalid index range. ")
        else:
            print("\nRecorded operations within the specified range: ")
            count = 1
            for i in range(from_index - 1, to_index):
                operation = recorded_operations[i]
                operation_type, product_name, price, quantity = operation
                print(f"\n{count}. \n- Type: {operation_type} \n- Product: {product_name} \n- Price: {price} \n- Quantity:{quantity}")
                count += 1
        
    except ValueError:
        print("\nError: Please enter a valid indices. ")



print("\nWelcome to the Monster Beverage Corporation!")
filename = input("Please provide the filename to read warehouse inventory: ")
data = load_data_from_file(filename + ".txt")
if isinstance(data, dict):
    account_balance = data.get("account_balance", 1000)
    recorded_operations = data.get("recorded_operations", [])
    warehouse_inventory = data.get("warehouse_inventory", {})

while True:
    print("\nAvailable commands: balance, sale, purchase, account, list, warehouse, review, end")
    command = input("\nEnter a command: ").lower()

    if command == "balance":
        manager.execute("balance")

    elif command == "sale":
        manager.execute("sale")


    elif command == "purchase":
        manager.execute("purchase")

    elif command == "account":
        manager.execute("account")

    elif command ==  "list":
        manager.execute("list")

    elif command == "warehouse":
        manager.execute("warehouse")

    elif command == "review":
        manager.execute("review")
            
    elif command == "end":
        # Save data to file before exiting
        save_data_to_file({
            "account_balance": account_balance,
            "recorded_operations": recorded_operations,
            "warehouse_inventory": warehouse_inventory
        }, filename + ".txt")
        print("\nGoodbye! Hope you have a nice day! ")
        break
    else:
        print("\nError: Please enter a valid command!")


