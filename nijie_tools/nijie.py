import sys, re, logging, requests, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path

login_page = "https://nijie.info/login.php"
popup_page = "https://nijie.info/view_popup.php?id="

logger = logging.getLogger('selenium')
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
logger.addHandler(handler)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
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

def GetImages(url):
    Login()
    image_links = []
    browser.get(url)
    artist = GetArtistName()
    gallery = browser.find_element(By.ID, "gallery")
    img = gallery.find_element(By.ID, "img_filter")
    illust_id = img.find_element(By.TAG_NAME, "img").get_attribute("illust_id")
    if illust_id != None:
        browser.get(popup_page+illust_id)
        for image in browser.find_element(By.ID, "img_window").find_elements(By.TAG_NAME, "img"):
            image_links.append(image.get_attribute("src"))
    else:
        video = img.find_element(By.TAG_NAME, "video")
        illust_id = video.get_attribute("illust_id")
        image_links.append(video.get_attribute("src"))
    
        
    print(image_links)
    SaveImages(image_links=image_links, artist=artist, illust_id=illust_id)

def GetArtistName():
    user = browser.find_element(By.CLASS_NAME, "user_icon")
    name = user.find_element(By.TAG_NAME, "img").get_attribute("alt")
    return name

def SaveImages(image_links, artist, illust_id):
    folderPath = "../downloads/nijie/"+artist+"/"+illust_id+"/"
    Path(folderPath).mkdir(parents=True, exist_ok=True)

    for image in image_links:
        fn, fe= FileInfo(image_link=image)
        with open(folderPath+fn+"."+fe, "wb") as of:
            of.write(requests.get(image).content)
            of.close()

def FileInfo(image_link):
    regex = r"/([^/]+)\.([a-zA-Z0-9]+)$"
    fi = re.search(regex, image_link)
    if fi:
        return fi.group(1), fi.group(2)
    else:
        print("Error: No match found for the filename and extension.")
        return None, None

def Run(args):
    print(args[1])
    GetImages(args[1])

Run(sys.argv)