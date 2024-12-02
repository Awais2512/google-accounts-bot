import requests
import os

sms_pool_api_key = 'UZ9nbTnX3dLKZjJLSxyJiIT4qZfiduhC'
def buy_phone():
    url = "https://api.smspool.net/purchase/sms"
    payload={
    'key': sms_pool_api_key,
    'country':'1',
    'service':'1476',
    'max_price':'2.00',
    'pricing_option':'1'
    }
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        return {"status": "ERROR", "message": "Failed to connect to the API"}
    
def check_phone(phone_id):
    url = "https://api.smspool.net/sms/check"

    payload={
    'key': sms_pool_api_key,
    'orderid':phone_id
    }

    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "ERROR", "message": "Failed to connect to the API"}
    
def get_sms_code(phone_id):
    try:
        response = check_phone(phone_id)
        # print(response)
        return response.get('sms')
    except:
        return None





import random
import string
import secrets
import random
from datetime import datetime, timedelta
from faker import Faker


# Function to generate a random date between two years
def generate_random_date(start_year=1990, end_year=2000):
    # Define the start and end date
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    # Calculate the total days between start and end date
    delta_days = (end_date - start_date).days

    # Generate a random number of days to add to the start date
    random_days = random.randint(0, delta_days)

    # Add the random number of days to start_date
    random_date = start_date + timedelta(days=random_days)

    # Return the date in dd-mm-yyyy format
    return random_date.strftime("%d-%m-%Y")

# Function to generate a random username
def generate_random_username(length=8):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# Function to generate a secure random password
def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Generate and print random username and password
random_username = generate_random_username()  # Adjust the length if needed
random_password = generate_secure_password()  # Adjust the length if needed
# Create a Faker instance
gender = random.choice(["male",'female'])
fake = Faker()

# Random first name
fname = fake.first_name_male() if gender =="male" else fake.first_name_female()
random_last_name = fake.last_name()  

# Print the names
print(f"Gender:{gender}")
print(f"Random First Name: {fname}")
print(f"Random Last Name: {random_last_name}")
print(f"Random Username: {random_username}")
print(f"Random Password: {random_password}")
# Generate and print a random date
random_date = generate_random_date()
print(f"Random Date: {random_date}")


import csv
import os

# Sample account_data dictionary
account_data = {
    "username": "larryhyuga231547",
    "password": "LarryHyuga@231547&",
    "firstName": "larry",
    "lastName": "hyuga",
    "dob": "22-03-1998",
    "gender": "male",
    "phone": "8704420528",
    "verification_code": "082530"
}

# Function to save data to a CSV file
def save_to_csv(data, file_name='account_data.csv'):
    # Define the column names
    fieldnames = data.keys()

    # Check if the file already exists
    file_exists = os.path.exists(file_name)

    # Open the CSV file in append mode ('a') and write the data
    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or os.path.getsize(file_name) == 0:
            writer.writeheader()  # Write the header if it's a new file

        # Write the account data as a row
        writer.writerow(data)

# Save the account_data to the CSV file

print("Data saved to account_data.csv")
