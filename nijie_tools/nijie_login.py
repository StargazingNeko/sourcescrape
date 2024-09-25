import json
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://nijie.info/login.php"

chrome_location = "/usr/bin/chromedriver"

options = webdriver.ChromeOptions()
options.binary_location = chrome_location
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

browser = webdriver.Chrome(options=options)
browser.get(url)
browser.implicitly_wait(30)
AcceptButton = browser.find_element(By.LINK_TEXT, "はい、私は18歳以上です")
AcceptButton.click()

Inputs = browser.find_elements(By.TAG_NAME, "input")

Email_Input = Inputs[0]
Password_Input = Inputs[1]
Login_Button = Inputs[2]

Email_Input.clear()
Email = input("Email:\n   ")
Email_Input.send_keys(Email) 
Password_Input.clear()
Passwd = input("Password:\n   ")
Password_Input.send_keys(Passwd)
Login_Button.click()

Cookies = browser.get_cookies()

with open("cookies", "w") as file:
    print(json.dump(Cookies, file, indent=4))
    file.close()

browser.close()
print("\nDone.")

