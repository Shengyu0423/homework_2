while True:
    try:
        max_items = int(input('\nPlease enter the number of items: '))
        break  # if user input the integer then break the loop
    except ValueError:
        print("\nError: Please enter a valid number.")

package_sent = 0
total_weight_sent = 0
total_weight_of_packages_sent = 0
total_unused_capacity = 0
max_unused_capacity = 0
max_unused_capacity_package = 0

package_capacity = 20  # maximum of each package

current_package_weight = 0
current_unused_capacity = 0

for i in range(1, max_items + 1):
    while True:
        try:
            item_weight = float(input(f"\nEnter the weight of item {i}: "))
            if item_weight < 0 or item_weight > 10:
                print('\nError: Weight should be within 1 to 10 kg.')    
            elif 0 < item_weight <= 10:
                if current_package_weight + item_weight > package_capacity: # if adding this item exceeds the package capacity
                    package_sent += 1
                    total_weight_sent += current_package_weight
                    total_weight_of_packages_sent += current_package_weight
                    total_unused_capacity += package_capacity - current_package_weight
                    current_unused_capacity = package_capacity - current_package_weight
                    if current_unused_capacity > max_unused_capacity:
                        max_unused_capacity = current_unused_capacity
                        max_unused_capacity_package = package_sent
                    print(f"\nPackage {package_sent} sent with item(s). Unused capacity: {current_unused_capacity} kg")
                    current_package_weight = 0  # start a new package
                current_package_weight += item_weight  # add the current item to the package
                if current_package_weight == package_capacity or i == max_items:  # if package is full or it's the last item
                    package_sent += 1
                    total_weight_sent += current_package_weight
                    total_weight_of_packages_sent += current_package_weight
                    total_unused_capacity += package_capacity - current_package_weight
                    current_unused_capacity = package_capacity - current_package_weight
                    if current_unused_capacity > max_unused_capacity:
                        max_unused_capacity = current_unused_capacity
                        max_unused_capacity_package = package_sent
                    print(f"\nPackage {package_sent} sent with item(s). Unused capacity: {current_unused_capacity} kg")
                    current_package_weight = 0  # start a new package
                break
        except ValueError:
            print("\nError: Please enter a valid number.")

print(f"\nTotal number of packages sent: {package_sent}")
print(f"\nTotal weight of packages sent: {total_weight_of_packages_sent} kg")
print(f"\nTotal unused capacity: {total_unused_capacity} kg")
print(f"\nPackage {max_unused_capacity_package} has the most unused capacity: {max_unused_capacity} kg")

