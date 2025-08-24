import json, time
from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://accounts.pixiv.net/login"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

browser = webdriver.Chrome(options=options)
browser.get(url)
browser.delete_all_cookies()
browser.implicitly_wait(30)

#UserID/Email input
user = browser.find_element(By.XPATH, '//*[@id="app-mount-point"]/div/div/div[4]/div[1]/div[2]/div/div/div/form/fieldset[1]/label/input')
user.clear()
user.send_keys(input("Email or PixivID:\n   "))

#Password input
passwd = browser.find_element(By.XPATH, '//*[@id="app-mount-point"]/div/div/div[4]/div[1]/div[2]/div/div/div/form/fieldset[2]/label/input')
passwd.clear()
passwd.send_keys(input("Password:\n   "))

time.sleep(5) #Wait for button to activate..?
#Log In button
click = browser.find_element(By.XPATH, '//*[@id="app-mount-point"]/div/div/div[4]/div[1]/div[2]/div/div/div/form/button[1]').click()
print(click)

time.sleep(10)
browser.save_screenshot("ss.png")
cookie = json.dumps(browser.get_cookie("PHPSESSID"), indent=4)
with open("cookies.json", "w") as file:
    file.write(cookie)
    file.close()

#browser.find_element(By.XPATH, '//*[@id="app-mount-point"]/div/div/div[4]/div[1]').screenshot("ss.png")
browser.quit()