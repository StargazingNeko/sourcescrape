import sys, ast, os, json, requests, re
from requests_html import HTMLSession
from pathlib import Path

def ScrapePixiv(url, id):
    _HtmlSession = HTMLSession()

    print("input:")
    print(url)
    r = _HtmlSession.get(url, headers=GetHeaders(), cookies=GetCookies())
    jstring = json.loads(r.html.find('#meta-preload-data')[0].attrs['content'])

    f = open("pixiv_auth", "a")
    if(os.stat("pixiv_auth").st_size == 0):
       f.close()

    return jstring['illust'][str(id)]["pageCount"], jstring['illust'][str(id)]['urls']['original'], jstring['illust'][str(id)]["userId"], jstring['illust'][str(id)]["userName"]

def GetHeaders():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': 'image/avif,image/webp,*/*',
    'Referer': 'https://www.pixiv.net/',
    }

    return headers

def GetCookies():
     cookies = ast.literal_eval(Path("cookies").read_text())
     cookiejar = requests.utils.cookiejar_from_dict(cookies)
     return cookiejar

def SaveImage(folder, url, id, page, data):
    print(folder+"/"+str(id)+"_p"+str(page)+"."+re.search(r"[^\.]+$", url)[0])
    with open(folder+"/"+str(id)+"_p"+str(page)+"."+re.search(r"[^\.]+$", url)[0], "wb") as fp:
        fp.write(data)
    return

def GetArtistId(url):
     return


def main(args):
    url = args[1]
    id = re.search(r"([^\/]+$)", url)[0]
    page_count, illust, artist_id, artist_name = ScrapePixiv(url, id)

    folder_path = "../downloads/pixiv/["+artist_id+"] "+artist_name
    if os.path.exists(folder_path) != True:
        Path(folder_path).mkdir(parents=True, exist_ok=True)

    if page_count == 1:
        data = requests.get(illust, headers=GetHeaders(), cookies=GetCookies())
        if data.status_code == 200:
            SaveImage(folder_path, illust, id, 0, data.content)
        else:
            print("Status Code returned " + str(data.status_code))
    else:
        page = 0
        for page in range(page, page_count):
            matches = re.search(r"(\d+_p)(\d)", illust)
            result = re.sub(r"(\d+_p)(\d)", matches[1]+str(page), illust, 1)
            data = requests.get(result, headers=GetHeaders(), cookies=GetCookies())
            if data.status_code == 200:
                SaveImage(folder_path, result, id, page, data.content)
            else:
                print("Status Code returned " + str(data.status_code))




main(sys.argv)