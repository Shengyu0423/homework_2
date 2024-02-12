# This is the personal Information
recipient_name = input("Tell me the recipent's name: ")
birth_year = int(input ("Which year you were born? "))
personalized_message = input("Anything that you would like to say? ")
sender_name = input("Tell me the sender's name? ")

# The definition of current year
current_year = 2024

# The calculation of the recipient's age
age = current_year - birth_year

# Print birthday card
print(f"\n{recipient_name}, let's celebrate your {age} years of awesomeness!") 
print(f"Wishing you a day filled with joy and laughter as you turn {age}!\n")
print(personalized_message)
print("\nWith love and best wishes,")
print(sender_name)


      
      
