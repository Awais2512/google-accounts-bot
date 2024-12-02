from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time 
from utils import *
from faker import Faker
sms_pool_api_key = os.getenv("SMS_POOL_API")


def get_driver():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
    chrome_options.add_argument("--incognito")  # Use incognito mode for fresh session
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True) #to keep chrome open
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def bot():
    dob = generate_random_date()
    date = dob.split("-")
    day_num = date[0]
    month_num = int(date[1])
    year_num = date[2]
    gender = random.choice(["male",'female'])
    fake = Faker()

    fname = fake.first_name_male() if gender =="male" else fake.first_name_female()
    lname = fake.last_name() 
    username = generate_random_username()
    pswd = generate_secure_password()
    print("username:",username)
    print("password:",pswd)
    print("firstName:",fname)
    print("lastName:",lname)
    print("dob:",dob)
    print("gender:",gender)

    driver = get_driver()

    try:
        # Open Google account creation page
        driver.get("https://accounts.google.com/signup")    

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        get_phone = buy_phone()
        phone_number = get_phone.get('phonenumber')
        phone_id = get_phone.get('order_id')

        if phone_number is None or phone_id is None:
            print("Failed to get phone number")
            return
        first_name_input = wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
        first_name_input.send_keys(fname)

        last_name_input = driver.find_element(By.ID, "lastName")
        last_name_input.send_keys(lname)
        
        next_button = driver.find_element(By.TAG_NAME,"button")
        next_button.click()
        wait.until(EC.visibility_of_element_located((By.ID,"month")))
        month = Select(driver.find_element(By.ID,"month"))
        month.select_by_index(month_num)
        day = driver.find_element(By.ID,"day")
        day.send_keys(day_num)
        year  = driver.find_element(By.ID,'year')
        year.send_keys(year_num)
        # time.sleep(2)
        gen = Select(driver.find_element(By.ID,"gender"))
        gen.select_by_visible_text(gender.capitalize())
        time.sleep(2)

        next_button = driver.find_element(By.TAG_NAME,"button")
        next_button.click()
        try:
            username_input = driver.find_element(By.CSS_SELECTOR, 'input[name="Username"]')
            username_input.send_keys(username)
        except:        
            driver.find_element(By.ID,"selectionc4").click()
            username_input = driver.find_element(By.CSS_SELECTOR, 'input[name="Username"]')
            username_input.send_keys(username)
        time.sleep(1)
        next_button = driver.find_element(By.TAG_NAME,"button")
        next_button.click()

        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(pswd)
        time.sleep(1)
        # # Confirm the password
        confirm_password_input = driver.find_element(By.NAME, "PasswdAgain")
        confirm_password_input.send_keys(pswd)

        next_button = driver.find_element(By.TAG_NAME, "button")
        next_button.click()
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        get_phone = buy_phone()
        phone_number = get_phone.get('phonenumber')
        phone_id = get_phone.get('order_id')

        if phone_number is None or phone_id is None:
            print("Failed to get phone number")
            return
        phone_input = driver.find_element(By.ID,"phoneNumberId")
        phone_input.send_keys(phone_number)
        time.sleep(3)
        next_button = driver.find_element(By.XPATH, "//button[@jsname='LgbsSe']")
        next_button.click()
        
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
        ver_code_input = driver.find_element(By.ID,"code")
        ver_code_input.send_keys(sms_code)
        time.sleep(1)
        next_button = driver.find_element(By.CSS_SELECTOR, 'button[jsname="LgbsSe"]')
        next_button.click()
        time.sleep(1)    
        try:  
            driver.find_element(By.ID,"recoveryEmailId")  
            driver.find_element(By.ID,"recoverySkip").find_element(By.TAG_NAME,"button").click()
            time.sleep(1)
            account_data ={
                "username":username,
                "password":pswd,
                "firstName":fname,
                "lastName":lname,
                "dob":dob,
                "gender":gender,
                "phone":phone_number,
                "verification_code":sms_code
            }
            save_to_csv(account_data)
        except:
            print("Error Recovery 1")
        try:
            # review = driver.find_element(By.XPATH,'//h1[@id="headingText"]').text
            # print(f"{review}:{username}")
            next_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button')
            next_button.click()            
            time.sleep(1)
        except:
            input("Review Error")
        next_button = driver.find_element(By.CSS_SELECTOR, 'button[jsname="LgbsSe"]')
        next_button.click()            
        time.sleep(1)
        # input("SColl page pause")
        while True:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("Scolling")
                time.sleep(1)
                agree_btn = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[1]/div/div/button')
                agree_btn.click()   
                break    
            except Exception as e:
                print("Error Scrolling",e)
        try:
            driver.find_element(By.CSS_SELECTOR,'button[jsname="ssJRIf"]').click()
        except:
            print("final confirm error 3")
        try:
            success_msg = driver.find_element(By.CSS_SELECTOR,'h1[class="XY0ASe"]').text
            print("SUcces:",success_msg)
        except:
            print("Error Success:")

    except Exception as e:
        print("Error:",e)

bot()
