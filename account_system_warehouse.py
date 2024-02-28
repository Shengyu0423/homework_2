warehouse_inventory = {
    "monster-original": {"price": 2, "quantities": 50},
    "monster-passionfruit": {"price": 2.5, "quantities": 30},
    "monster-mango": {"price": 2.5, "quantities": 30},
    "monster-kiwi": {"price": 3, "quantities": 20},
    "monster-citrus": {"price": 3.5, "quantities": 15}
}

account_balance = 1000

recorded_operations = [] #save all the operation

while True:
    print("\nWelcome to the Monster Beverage Corportation!")
    print("\nAvailable commands: balance, sale, purchase, account, list, warehouse, review, end")
    command = input("\nEnter a command: ").lower()

    if command == "balance":
        try:
           amount = float(input("\nPlease add or subtract the amount to the account: "))
           account_balance += amount
           print(f"\nUpdated account balance: {account_balance}")
        except ValueError:
           print("\nError: Please enter a valid amount. ")

    elif command =="sale":
        try:
            product_name = input("\nPlease enter the product name: ")
            if product_name in warehouse_inventory:
                price = float(input("\nPlease enter the price per unit: "))
                quantity = int(input("\nPlease enter the quantity sold: "))

            # Check whether the quantities of products in warehouse are enough to sale 
                if warehouse_inventory[product_name]["quantities"] >=quantity:
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
                print("\n Error: Invalid product name!")
        except ValueError:
            print("\nPlease enter a valid input for product name, price and quantity. ")

    elif command == "purchase":
        try:
            product_name = input ("\nPlease enter the product name: ")
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
                    print("\nError: Inalid quantity for purchase!")
            else:
                # Ask user to provide deatils of new product
                print("\nProduct not found in inventory. Please provide the following information: ")
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
                    else:
                        print("\nError: Insufficient account balance for purchase!")
                else:
                    print("\nError: Inalid quantity for purchase!")

        except ValueError:
            print("\nError: Please enter valid inputs for price and quantity. ")

    elif command == "account":
        print(f"\nCurrent account balance: {account_balance}")

    elif command ==  "list":
        print("\nWarehouse Inventory:\n ")
        for item, details in warehouse_inventory.items():
            print(f"{item.capitalize()}:")
            for detail, value in details.items():
                print(f"- {detail.capitalize()}: {value}")

    elif command == "warehouse":
        product_name = input("\nPlease enter one of the products to check details: ")
        if product_name in warehouse_inventory:
            print(f"\nProduct: {product_name.capitalize()}")
            for detail, value in warehouse_inventory[product_name].items():
                print(f"- {detail.capitalize()}: {value}")
        else:
            print("\nError: Product not found in warehouse! ")

    elif command == "review":
        try:
            from_index = input("\nEnter the 'from' index: ")
            to_index = input("\nEnter the 'to' index: ")

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
            
    elif command == "end":
        print("\nGoodbye! Hope you have a nice day! ")
        break
    else:
        print("\nError: Please enter a valid command!")