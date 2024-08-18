import sys, re, logging, time, os, requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from pathlib import Path

logger = logging.getLogger('selenium')
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
logger.addHandler(handler)

chrome_location = "/usr/bin/chromedriver"
chrome_driver_binary = "/usr/bin/chromedriver"
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

def Main(args):
    Run(args[1])

def Run(args):
    browser.get(args)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2) 
    browser.implicitly_wait(20)
    content = browser.page_source
    tweet_photo_link = []
    cleaned_photo_link = []
    soup = bs(content, 'html.parser')

    userName, userHandle = GetUserInfo(soup)
    
    for _ in soup.find_all('div', {'data-testid': 'tweetPhoto'}):
        for img in _.find_all('img', {'alt': 'Image'}):
            tweet_photo_link.append(img.get('src'))

    regex_string = r".(?<=\?)[^']+(?=.)."
    regex_ext_string = r"\?format=([^&]*)"
    regex_filename = r"\/([^\/:]*):"

    for link in tweet_photo_link:
        ext = re.search(regex_ext_string, link)[1]
        img_link = re.sub(regex_string, "."+ext+":orig", link)
        print(img_link)
        if img_link not in cleaned_photo_link:
            cleaned_photo_link.append(img_link)
            SaveImage("downloads/twitter/["+userHandle+"]"+userName, re.search(regex_filename, img_link)[1], requests.get(img_link).content)





    End()

def GetUserInfo(in_soup):
    user = []

    for _ in in_soup.find_all('div', {'data-testid': 'User-Name'}):
        for text in _.find_all('span'):
            if text not in user:
                user.append(text.get_text())

    return user[0], user[3]

def End():
    browser.quit()

def SaveImage(folder, name, data):
    if os.path.exists("downloads/twitter") != True:
        Path("downloads/twitter").mkdir()
        Path(folder).mkdir()
    elif os.path.exists(folder) != True:
        print(folder)
        Path(folder).mkdir()
    else:
        print("Location exists.")
    
    save_location = folder+"/"+name

    with open(save_location, "wb") as fp:
        print(save_location)
        fp.write(data)
    return

Main(sys.argv)