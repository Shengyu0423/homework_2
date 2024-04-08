import requests
import datetime
import csv
import os

# Writing the data into rain_forecast.csv file
def save_data_to_file():
    # Check if the data already exists for the same date
    with open('rain_forecast.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == user_date_input:
                print("Data for the same date already exists in the CSV file.")
                return
    # If data does not exist, write it to the file        
    with open('rain_forecast.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_date_input, precipitation])

# Reading the data from rain_forecast.csv file
def load_data_from_file():
    with open('rain_forecast.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == user_date_input:
                precipitation = float(row[1])
                if precipitation > 0:
                    print(f"\nIt will rain and the precipitation will be: {precipitation}")
                elif precipitation == 0:
                    print(f"\nIt will not rain")
                else:
                    print("\nI don't know")
                return

if not os.path.exists('rain_forecast.csv'):
    with open('rain_forecast.csv', 'w', newline='') as file:
        pass

while True:
        # Ask user for a date
        user_date_input = input("\nPlease input for a date in YYYY-mm-dd format to check the weather in Dublin: ")
        if not user_date_input.strip():
            user_date = datetime.datetime.now() + datetime.timedelta(days=1)
            user_date_input = user_date.strftime('%Y-%m-%d')
            print(f"Checking tomorrow's weather ({user_date_input})...")
            url =  f"https://api.open-meteo.com/v1/forecast?latitude=53.3331&longitude=-6.2489&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={user_date_input}&end_date={user_date_input}"
            response = requests.get(url)
            response_dict = response.json()
            if "daily" in response_dict:
                daily_data = response_dict["daily"]
                if "precipitation_sum" in daily_data:
                    precipitation = daily_data['precipitation_sum'][0]
                    if precipitation > 0:
                       print(f"\nIt will rain and the precipitation will be: {precipitation}")
                    elif precipitation == 0:
                        print("\nIt will not rain")
                    else:
                        print("\nI don't know")
                else:
                    print("\nNo precipitation data available for the specified date.")
            else:
                print("\nSorry, cannot obtain the data successfully.")
            save_data_to_file()
            break
        else:
            try:
                # Covert the user input to a datetime object 
                user_date = datetime.datetime.strptime(user_date_input, '%Y-%m-%d')

                # Check if CSV file conatins data for the same date
                date_exists = False
                with open('rain_forecast.csv', 'r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row and row[0] == user_date_input:
                            date_exists = True
                            break

                if date_exists:
                    print("\nData for the same date already exists in CSV file.")
                    load_data_from_file()
                    break
                else:
                    print("\nNo data found for the specified date in CSV file. Proceeding to fetch data from API...")
                    url =  f"https://api.open-meteo.com/v1/forecast?latitude=53.3331&longitude=-6.2489&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={user_date_input}&end_date={user_date_input}"
                    response = requests.get(url)
                    response_dict = response.json()
                    if "daily" in response_dict:
                        daily_data = response_dict["daily"]
                        if "precipitation_sum" in daily_data:
                            precipitation = daily_data['precipitation_sum'][0]
                            if precipitation > 0:
                                print(f"\nIt will rain and the precipitation will be: {precipitation}")
                            elif precipitation == 0:
                                print(f"\nIt will not rain")
                            else:
                                print("\nI don't know")
                        else:
                            print("\nNo precipitation data available for the specified date.")
                    else:
                        print("\nSorry, cannot obtain the data successfully.")
                    
                    save_data_to_file()
                    break
            except ValueError:
                print("\nInvalid date format. Please input the date in YYYY-mm-dd format.")



