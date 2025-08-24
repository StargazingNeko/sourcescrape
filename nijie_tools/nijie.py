import sys, re, logging, requests, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path

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
    browser.get("https://nijie.info/login.php")
    with open("cookies", "r") as cookie_file:
        cookies = json.load(cookie_file)
        cookie_file.close()

    for cookie in cookies:
        browser.add_cookie(cookie)
        
    browser.refresh()

def GetNijiePopup(illust_id):
    browser.get("https://nijie.info/view_popup.php?id="+illust_id)

def GetMedia(url):
    print(url)
    Login()
    media_links = []
    browser.implicitly_wait(2)
    browser.get(url)
    artist = GetArtistName()
    if artist != None:      
        illust_id, media_links = GetVideo()
        if illust_id != None:
            SaveImages(image_links=media_links, artist=artist, illust_id=illust_id)
            return
        
        illust_id, media_links = GetGallery()
        if illust_id != None:
            SaveImages(image_links=media_links, artist=artist, illust_id=illust_id)
            return
        
        illust_id, media_links = GetDoujin()
        if illust_id != None:
            SaveImages(image_links=media_links, artist=artist, illust_id=illust_id)
            return
        
        print("Possible unsupported page, open a ticket on github with the id.")
    else:
        print("Open an issue ticket on github.")

def GetArtistName():
    user = browser.find_elements(By.CLASS_NAME, "user_icon")
    if len(user) != 0:
        user = user[0]
        name = user.find_element(By.TAG_NAME, "img").get_attribute("alt")
        print("Artist: "+name)
        return name
    else:
        try:       
            name = browser.find_element(By.XPATH, '//*[@id="dojin_left"]/div[3]/p/a/span').text
            return name
        except:
            print("Could not get the artist name, it's possible this page is not supported yet.")
            return None

def GetGallery(illust_id = None):
    print("Checking for gallery.")
    image_links = []
    if illust_id == None:
        try:
            illust_id = browser.find_element(By.ID, "gallery").find_element(By.ID, "img_filter").find_element(By.TAG_NAME, "img").get_attribute("illust_id")
        except:
            return None, None
    
    print("Detected gallery.")
    print(illust_id)
    GetNijiePopup(illust_id)
    for image in browser.find_element(By.ID, "img_window").find_elements(By.TAG_NAME, "img"):
        if  CheckForBlacklistedContent(image.get_attribute("src")) == False:
            image_links.append(image.get_attribute("src"))
    return illust_id, image_links

def GetVideo():
    print("Checking for video(s)")
    video_links = []
    videos = browser.find_elements(By.TAG_NAME, "video")
    if len(videos) == 0:
        return None, None
    
    print("Detected video(s)")
    illust_id = videos[0].get_attribute("illust_id")
    print(illust_id)
    for video in videos:
        video_links.append(video.get_attribute("src"))
    return illust_id, video_links

def GetDoujin():
    print("Checking for Doujin")
    try:
        dojin_panel = browser.find_element(By.ID, "dojin_left")
        print("Doujin detected.")
        illust_id = dojin_panel.find_element(By.ID, "dojin_diff").find_element(By.TAG_NAME, "img").get_attribute("illust_id")
        print(illust_id)
        return GetGallery(illust_id)
    except: 
        return None, None

#NOTE: This will never be used for censorship or preventing you from saving a specific album/gallery.
#It will only ever be used in the cases that unwanted media such as the sites filters for whatever reason gets included.
#Censorship regardless of morals, reasoning, and what not is horrendous and immoral in itself!
def CheckForBlacklistedContent(item):
    blacklist = ["https://nijie.info/pic/filter/width/1.png"]
    if item in blacklist:
        return True
    else:
        return False

def SaveImages(image_links, artist, illust_id):
    print(image_links)
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
    GetMedia(args[1])
    browser.quit()

Run(sys.argv)