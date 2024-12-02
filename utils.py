import requests
import os , csv
import random
import string
import secrets
import random , os
from datetime import datetime, timedelta
from faker import Faker
from dotenv import load_dotenv
load_dotenv()

sms_pool_api_key = os.getenv("SMS_POOL_API")


def buy_phone():
    url = "https://api.smspool.net/purchase/sms"
    payload={
    'key': sms_pool_api_key,
    'country':'1',
    'service':'395',
    # 'max_price':'2.00',
    # 'pricing_option':'1'
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

def generate_random_date(start_year=1990, end_year=2000):
    
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%d-%m-%Y")

def generate_random_username(length=8):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def save_to_csv(data, file_name='account_data.csv'):
    # Define the column names
    fieldnames = data.keys()
    file_exists = os.path.exists(file_name)
    # Open the CSV file in append mode ('a') and write the data
    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or os.path.getsize(file_name) == 0:
            writer.writeheader()  # Write the header if it's a new file

        # Write the account data as a row
        writer.writerow(data)


# # Generate and print random username and password
# random_username = generate_random_username()  # Adjust the length if needed
# random_password = generate_secure_password()  # Adjust the length if needed
# # Create a Faker instance
# gender = random.choice(["male",'female'])
# fake = Faker()

# # Random first name
# fname = fake.first_name_male() if gender =="male" else fake.first_name_female()
# random_last_name = fake.last_name()  

# # Print the names
# print(f"Gender:{gender}")
# print(f"Random First Name: {fname}")
# print(f"Random Last Name: {random_last_name}")
# print(f"Random Username: {random_username}")
# print(f"Random Password: {random_password}")
# # Generate and print a random date
# random_date = generate_random_date()
# print(f"Random Date: {random_date}")

