from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import requests
import os
import time

sms_pool_api_key = 'UZ9nbTnX3dLKZjJLSxyJiIT4qZfiduhC'
excel_file = 'input.xlsx'
records = []
import random
import string

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "outlook.com"]
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for i in range(10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

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

def read_records():
    if os.path.exists(excel_file):
        # Read the Excel file
        df = pd.read_excel(excel_file, engine='openpyxl')

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            record = {
                'First Name': row['FIRST'],
                'Last Name': row['LAST'],
                'DOB': row['DOB'],
                'primary_address': row['Patient Primary Address'],
                'ZIP': row['ZIP'],
                'City': row['City'],
                'State': row['State'],
                'Rx': row['Rx Number']
            }
            # Append the record to the list
            records.append(record)
    else:
        print(f"Error: File '{excel_file}' not found")

def print_records():
    # Display the extracted data (for demonstration)
    for i, record in enumerate(records, 1):
        print(f"Record {i}: | First Name: {record['First Name']} | Last Name: {record['Last Name']} | DOB: {record['DOB']} | Primary Address: {record['primary_address']} | ZIP: {record['ZIP']} | City: {record['City']}\n")


def bot(record):
    print(f"First Name: {record['First Name']} | Last Name: {record['Last Name']} | DOB: {record['DOB']} | Primary Address: {record['primary_address']} | ZIP: {record['ZIP']} | City: {record['City']} | Rx Number: {record['Rx']}\n")
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)
    driver.get("https://www.enrollment.zepbound.lilly.com/enroll/checkEnrollment")
    try:
        time.sleep(5)
        accept_button = wait.until(EC.presence_of_element_located((By.ID, "cassie_accept_all_pre_banner")))
        accept_button.click()
        print("Accept All Cookies button clicked")
        DOB = record['DOB'].strftime('%m,%d,%Y')
        DOB = DOB.replace(',', '/')
        dob_input = wait.until(EC.presence_of_element_located((By.ID, 'dob-enrollment')))
        actions.move_to_element(dob_input).click().send_keys(DOB).perform()

        #get a phone number and its order id
        get_phone = buy_phone()
        phone_number = get_phone.get('phonenumber')
        phone_id = get_phone.get('order_id')
        # phone_number = '4064015339'
        # phone_id = 'HKP9ZQDA'

        if phone_number is None or phone_id is None:
            print("Failed to get phone number")
            return

        phone_input = wait.until(EC.presence_of_element_located((By.ID, 'phone-enrollment')))
        actions.move_to_element(phone_input).click().send_keys(phone_number).perform()

        
        send_verification_code = wait.until(EC.presence_of_element_located((By.ID, 'sendCodeButton')))
        send_verification_code.click()

        timeout = 10 * 60  # 10 minutes in seconds
        interval = 30  # check every 30 seconds
        start_time = time.time()
        sms_code = None
        time.sleep(5)
        #code to check if verification code is received with retries and intervals
        while (time.time() - start_time) < timeout:
            sms_code = get_sms_code(phone_id)
            if sms_code:
                print("SMS code found:", sms_code)
                break
            print("SMS code not found. Retrying in 30 seconds...")
            time.sleep(interval)

        if not sms_code:
            print("Failed to get SMS code within 10 minutes.")
            return

        code_input = wait.until(EC.presence_of_element_located((By.ID, 'code')))
        actions.move_to_element(code_input).click().send_keys(sms_code).perform()

        continue_button = wait.until(EC.element_to_be_clickable((By.ID, 'positive')))
        continue_button.click()
        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='resident-1']")))
        label.click()
        print("Label clicked.")
        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='insurance-1']")))
        label.click()
        print("Label clicked.")
        continue_button = wait.until(EC.element_to_be_clickable((By.ID, 'positive')))
        continue_button.click()
        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='indication']")))
        label.click()
        print("Label clicked.")
        continue_button = wait.until(EC.element_to_be_clickable((By.ID, 'positive')))
        continue_button.click()
        first_name = wait.until(EC.presence_of_element_located((By.ID, 'fname')))
        actions.move_to_element(first_name).click().send_keys(record['First Name']).perform()
        last_name = wait.until(EC.presence_of_element_located((By.ID, 'lname')))
        actions.move_to_element(last_name).click().send_keys(record['Last Name']).perform()
        email = generate_random_email()
        email_input = wait.until(EC.presence_of_element_located((By.ID, 'email')))
        actions.move_to_element(email_input).click().send_keys(email).perform()
        re_email_input = wait.until(EC.presence_of_element_located((By.ID, 'confirmEmail')))
        actions.move_to_element(re_email_input).click().send_keys(email).perform()
        address = wait.until(EC.presence_of_element_located((By.ID, 'address')))
        actions.move_to_element(address).click().send_keys(record['primary_address']).perform()
        city = wait.until(EC.presence_of_element_located((By.ID, 'city')))
        actions.move_to_element(city).click().send_keys(record['City']).perform()
        state = wait.until(EC.presence_of_element_located((By.ID, 'state')))
        select = Select(state)
        select.select_by_visible_text(record['State'])
        zip_code = wait.until(EC.presence_of_element_located((By.ID, 'zip')))
        actions.move_to_element(zip_code).click().send_keys(record['ZIP']).perform()
        select_element = wait.until(EC.presence_of_element_located((By.ID, "deliveryMethod")))
        select = Select(select_element)
        select.select_by_visible_text("Text")
        print("Text selected.")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/div/div[1]/div[11]/div/div[2]/button")))
        submit_button.click()
        print("Submit button clicked.")
        start_signing = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/button")))
        start_signing.click()
        print("Start signing button clicked.")
        adopt_sign = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div/form/div/div/div[3]/div[2]/button[1]")))
        adopt_sign.click()
        print("Adopt Sign button clicked.")
        text_sign = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[1]/div[1]/div/div[1]/label")))
        text_sign.click()
        adopt_sign = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[2]/button[1]")))
        adopt_sign.click()
        print("Adopt Sign button clicked.")
        apply_sign = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div/form/div/div/div[4]/div[1]/button[1]")))
        apply_sign.click()
        print("Apply Sign button clicked.")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div/button[2]")))
        submit_button.click()
        print("Submit button clicked.")
        code = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/dl/div[4]/dd')))
        code = code.text
        print("Code:", code)
        file_is_empty = False
        if not os.path.exists('output.csv'):
            file_is_empty = True
        with open('output.csv', 'a') as file:
            if file_is_empty:
                file.write(f"First Name,Last Name,DOB,Primary Address,ZIP,City,State,Rx Number,Code ID\n")
            # Write record data
            file.write(f"{record['First Name']},{record['Last Name']},{DOB},{record['primary_address']},{record['ZIP']},{record['City']},{record['State']},{record['Rx']},{code}\n")
        # input("Press to continue...")

    except Exception as e:
        print("Something Went Wrong:", e)
        input("Press ENTER to continue...")
    finally:
        driver.quit()

read_records()
# print_records()
print('Processing record...')
for record in records:
    bot(record)
print('Record processed successfully')
