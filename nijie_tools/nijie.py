import sys, re, logging, requests, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path

login_page = "https://nijie.info/login.php"
direct_image_link = ""
FileName, FileExt = "",""

logger = logging.getLogger('selenium')
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
logger.addHandler(handler)

chrome_location = "/usr/bin/chromedriver"
firefox_location = "/snap/firefox/current/usr/lib/firefox/firefox"

options = webdriver.ChromeOptions()
options.binary_location = chrome_location
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

browser = webdriver.Chrome(options=options)

def Login():
    browser.get(login_page)
    with open("cookies", "r") as cookie_file:
        cookies = json.load(cookie_file)
        cookie_file.close()

    for cookie in cookies:
        browser.add_cookie(cookie)
        
    browser.refresh()

def GetImage(url):
    global direct_image_link, FileName, FileExt
    browser.get(url)
    gallery = browser.find_element(By.ID, "gallery")
    direct_image_link = gallery.find_element(By.TAG_NAME, "img").get_attribute("src")
    print(direct_image_link)
    FileName, FileExt = FileInfo()

def GetArtistName():
    user = browser.find_element(By.CLASS_NAME, "user_icon")
    name = user.find_element(By.TAG_NAME, "img").get_attribute("alt")
    return name

def SaveImage(artist, fn, fe):
    folderPath = "downloads/"+artist+"/"
    p = Path(folderPath)
    p.mkdir(parents=True, exist_ok=True)

    with open(folderPath+fn+"."+fe, "wb") as image:
        image.write(requests.get(direct_image_link).content)
        image.close()

def FileInfo():
    regex = r"/([^/]+)\.([a-zA-Z0-9]+)$"
    fi = re.search(regex, direct_image_link)
    if fi:
        return fi.group(1), fi.group(2)
    else:
        print("Error: No match found for the filename and extension.")
        return None, None

def Run(args):
    Login()
    print(args[1])
    GetImage(args[1])
    Artist = GetArtistName()
    browser.quit()
    SaveImage(Artist, FileName, FileExt)

Run(sys.argv)